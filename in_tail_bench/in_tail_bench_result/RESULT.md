# in_tail benchmark results

## Environment

* Collector
  * CentOS 8 on AWS t2.medium instance
* Aggregator
  * CentOS 8 on AWS t2.medium instance

## Benchmark Scenario

* increase generating lines rate step by step
  * baseline(0 line/sec)
  * 500 lines/sec
  * 1000 lines/sec
  * 2000 lines/sec
  * 5000 lines/sec
* Generate logs with [dummer](https://github.com/sonots/dummer)
* Dummer generates ltsv format lines:
```
# dummer.conf
configure 'sample' do
  output "message.log"
  delimiter "\t"
  labeled true
  field :id, type: :integer, countup: true, format: "%04d"
  field :time, type: :datetime, format: "[%Y-%m-%d %H:%M:%S]", random: false
  field :level, type: :string, any: %w[DEBUG INFO WARN ERROR]
  field :method, type: :string, any: %w[GET POST PUT]
  field :uri, type: :string, any: %w[/api/v1/people /api/v1/textdata]
  field :reqtime, type: :float, range: 0.1..5.0
  field :foobar, type: :string, length: 8
end
```

## Fluentd Configurations for benchmarking

### Collector configuration

```
in_tail ------> out_forword -----> [aggregator node]
```


```aconf
<source>
  @type tail
  @id tail
  tag raw.tail
  path "#{ENV['HOME']}/message.log"
  pos_file "#{ENV['HOME']}/message.log.pos"
  <parse>
    @type ltsv
  </parse>
</source>

<match **>
  @type forward
  <server>
    host 10.1.3.4
    port 24224
  </server>
  <buffer>
    @type file
    flush_interval 2s
    path ./tmp/buffer
  </buffer>
</match>
```

### Aggregator configuration

```
[collector node] ------> in_forword -----> out_stdout
```

```aconf
<source>
  @type forward
</source>
<match **>
  @type stdout
</match>
```

## Results -- Boxplots

### Calyptia-Fluentd

#### CPU usage -- Supervisor

![Calyptia-Fluentd CPU Usage on supervisor](Calyptia-Fluentd-CPU_usage_on_supervisor.png)

CPU usage of Fluentd supervisor is around zero.

#### CPU usage -- Worker

![Calyptia-Fluentd CPU Usage on worker](Calyptia-Fluentd-CPU_usage_on_worker.png)

CPU usage of Fluentd worker corresponds to flow rate.
(This plot does not adjust with CPU counts.)

#### RSS usage -- Supervisor

![Calyptia-Fluentd RSS Usage on supervisor](Calyptia-Fluentd-RSS_usage_on_supervisor.png)

RSS usage of Fluentd supervisor is almost same.
This plot uses actual values of RSS.

#### RSS usage -- Worker

![Calyptia-Fluentd RSS Usage on worker](Calyptia-Fluentd-RSS_usage_on_worker.png)

RSS usage of Fluentd worker weakly corresponds to flow rate.
This plot uses actual values of RSS.

#### VMS usage -- Supervisor

![Calyptia-Fluentd-VMS Usage on supervisor](Calyptia-Fluentd-VMS_usage_on_supervisor.png)

VMS usage of Fluentd supervisor is almost same.
This plot uses actual values of VMS.

#### VMS usage -- Worker

![Calyptia-Fluentd-VMS Usage on worker](Calyptia-Fluentd-VMS_usage_on_worker.png)

VMS usage of Fluentd supervisor is almost same.
This plot uses actual values of VMS.

### Td-Agent

#### CPU usage -- Supervisor

![Td-Agent CPU Usage on supervisor](Td-Agent-CPU_usage_on_supervisor.png)

CPU usage of Fluentd supervisor is around zero.

#### CPU usage -- Worker

![Td-Agent CPU Usage on worker](Td-Agent-CPU_usage_on_worker.png)

CPU usage of Fluentd worker corresponds to flow rate.
(This plot does not adjust with CPU counts.)

#### RSS usage -- Supervisor

![Td-Agent RSS Usage on supervisor](Td-Agent-RSS_usage_on_supervisor.png)

RSS usage of Fluentd supervisor is almost same.
This plot uses actual values of RSS.

#### RSS usage -- Worker

![Td-Agent RSS Usage on worker](Td-Agent-RSS_usage_on_worker.png)

RSS usage of Fluentd worker weakly corresponds to flow rate.
This plot uses actual values of RSS.

#### VMS usage -- Supervisor

![Td-Agent-VMS Usage on supervisor](Td-Agent-VMS_usage_on_supervisor.png)

VMS usage of Fluentd supervisor is almost same.
This plot uses actual values of VMS.

#### VMS usage -- Worker

![Td-Agent-VMS Usage on worker](Td-Agent-VMS_usage_on_worker.png)

VMS usage of Fluentd supervisor is almost same.
This plot uses actual values of VMS.

### Comparision with Lineplot

#### CPU usage -- Supervisor

![Compare with CPU usage on supervisor](LinePlot-CPU_usage_on_supervisor.png)

CPU usages on supervisor are almost around zero.

#### CPU usage -- Worker

![Compare with CPU usage on supervisor](LinePlot-CPU_usage_on_worker.png)

CPU usages on worker almost denote the same tendency.
But, in high traffic ratio environment, Calyptia-Fluentd uses slightly bits lower CPU time consumption.

#### RSS usage -- Supervisor

![Compare with RSS on supervisor](LinePlot-RSS_usage_on_supervisor.png)

RSS usages on supervisor are almost same in both of agents.

#### RSS usage -- Worker

![Compare with RSS usage on supervisor](LinePlot-RSS_usage_on_worker.png)

Td-Agent uses more RSS.
When using Calyptia-Fluentd, RSS usage is declined against using Td-Agent with same configuration.

#### VMS usage -- Supervisor

![Compare with VMS usage on supervisor](LinePlot-VMS_usage_on_supervisor.png)

VMS usages on supervisor are almost same in both of agents.

#### Private Bytes Set usage -- Worker

![Compare with VMS Set usage on supervisor](LinePlot-VMS_usage_on_worker.png)

Working Set usages on worker denote the same tendency per agents (td-agent vs. calyptia-fluentd).
Calyptia-Fluentd uses slightly more Working Set.

## Conclusion

* Worker Process
  * `in_tail` resource usage for flat file, which steadily growing with fixed flow rate, corresponds to:
     * Flow rate
   * Calyptia-Fluentd's CPU usage is almost same, but slightly reduced CPU usage in high loaded case (tailing 5000 lines/sec).
   * Calyptia-Fluentd's memory usage is lower than TD-Agent.
* Supervisor process just monitors  life-and-death of worker process(es)
