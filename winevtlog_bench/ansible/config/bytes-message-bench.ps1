Param(
    [string]$workdir = "C:\tools",
    [parameter(mandatory=$true)][int32]$Length,
    [int32]$Total = 120000,
    [string]$PackageName = "calyptia-fluentd"
)

$ENV:PATH="C:\opt\" + $PackageName + "\bin;" + $ENV:PATH

cd $workdir

# Stop Fluentd service if exists
$count = (Get-Service -Name fluentdwinsvc -ErrorAction SilentlyContinue).Count
if ($count -ge 1) {
    Get-Service -Name fluentdwinsvc -ErrorAction SilentlyContinue | Stop-Service
    while ($true) {
	$count = (Get-Process -Name ruby -ErrorAction SilentlyContinue).Count
	if ($count -eq 0) {
            break
	}
	Start-Sleep 1
    }
}

Start-Process fluentd -ArgumentList "-c", "C:\opt\$PackageName\fluent-collector.conf", "-o", "C:\opt\$PackageName\message-$PackageName-$Length-bytes.log" -NoNewWindow -PassThru

while ($true) {
    $count = (Get-Process -Name ruby -ErrorAction SilentlyContinue).Count
    if ($count -ge 2) {
        break
    }
    Start-Sleep 1
}

while($true) {
    $instances = (Get-Counter "\Process(*)\% Processor Time" -ErrorAction SilentlyContinue).CounterSamples | select InstanceName | select-string "ruby"
    if ($instances.Count -ge 2) {
        break
    }
    Start-Sleep 1
}

Start-Process typeperf -ArgumentList "-cf", "counters.txt", "-sc", "2400", "-si", "1" -PassThru -RedirectStandardOutput C:\tools\${Length}-${PackageName}-resource-usage.csv

$socket_count_job = Start-Process powershell -ArgumentList "-ExecutionPolicy", "RemoteSigned", C:\tools\socket-count.ps1 -PassThru -NoNewWindow -RedirectStandardOutput C:\tools\${Length}-${PackageName}-socket-usage.csv

Start-Process C:\tools\EventLogBencher\EventLogBencher.exe -ArgumentList "wait", "-w", "50", "-t", "$Total", "-l", "$Length" -Wait -NoNewWindow

Stop-Process -Id $socket_count_job.Id
taskkill /F /IM ruby.exe
taskkill /F /IM typeperf.exe
