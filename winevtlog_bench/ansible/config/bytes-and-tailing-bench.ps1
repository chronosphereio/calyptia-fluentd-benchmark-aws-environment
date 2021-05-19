Param(
    [string]$workdir = "C:\tools",
    [int32]$Total = 1000,
    [string]$PackageName = "calyptia-fluentd",
    [parameter(mandatory=$true)][int32]$Length,
    [parameter(mandatory=$true)][int32]$BatchSize,
    [parameter(mandatory=$true)][int32]$LineRate
 )

$ENV:PATH="C:\opt\" + $PackageName + "\bin;" + $ENV:PATH

cd $workdir

Start-Process fluentd -ArgumentList "-c", "C:\opt\$PackageName\fluent-collector-with-tailing.conf", "-o", "C:\opt\$PackageName\message-$PackageName-$BatchSize-events-and-$LineRate-lines.log" -NoNewWindow -PassThru

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

Start-Process typeperf -ArgumentList "-cf", "counters.txt", "-sc", "2400", "-si", "1" -PassThru -RedirectStandardOutput C:\tools\${PackageName}-${BatchSize}events-${LineRate}lines-resource-usage.csv

$socket_count_job = Start-Process powershell -ArgumentList "-ExecutionPolicy", "RemoteSigned", C:\tools\socket-count.ps1 -PassThru -NoNewWindow -RedirectStandardOutput C:\tools\${PackageName}-${BatchSize}events-${LineRate}lines-socket-usage.csv

Start-Process C:\tools\EventLogBencher\EventLogBencher.exe -ArgumentList "batch", "-b", "$BatchSize", "-t", "$Total", "-l", "$Length" -PassThru -NoNewWindow

Start-Process C:\tools\FileLoggingBencher\FileLoggingBencher.exe -ArgumentList "-r", "$LineRate", "-o", "C:\\tools\\dummy.log", "-t", "$Total" -Wait -NoNewWindow

Stop-Process -Id $socket_count_job.Id
taskkill /F /IM ruby.exe
taskkill /F /IM typeperf.exe
# Delete flat file and its position file.
Remove-Item 'C:\tools\dummy.log*'
