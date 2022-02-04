#!/usr/bin/env python3

import psutil
import time
from datetime import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("steps", help="Total running seconds",
                    type=int)
parser.add_argument("agent", help="Specify agent package name",
                    type=str)
args = parser.parse_args()


class ProcessMetrics:
    process = None

    def __init__(self, process):
        self.process = process

    def memory_metrics(self):
        meminfo = self.process.memory_full_info()
        rss = meminfo.rss
        vms = meminfo.vms

        return rss, vms

    def cpu_percent(self):
        return self.process.cpu_percent(interval=1)


class IOMetrics:
    def __init__(self):
        self._last_disk_io_cache = (0, 0, 0.0)
        self._last_net_io_cache  = (0, 0, 0.0)

    def disk_io_metrics(self):
        disk_counters = psutil.disk_io_counters()
        tm = time.time()

        read_bytes = disk_counters.read_bytes
        write_bytes = disk_counters.write_bytes

        last_read_bytes, last_write_bytes, last_time = self._last_disk_io_cache
        delta = tm - last_time
        read_speed = (read_bytes - last_read_bytes) / delta
        write_speed = (write_bytes - last_write_bytes) / delta

        self._last_disk_io_cache = (read_bytes, write_bytes, tm)
        return write_speed, read_speed

    def net_io_metrics(self):
        net_counters = psutil.net_io_counters()
        tm = time.time()

        send_bytes = net_counters.bytes_sent
        recv_bytes = net_counters.bytes_recv

        last_send_bytes, last_recv_bytes, last_time = self._last_net_io_cache
        delta = tm - last_time
        recv_speed = (recv_bytes - last_recv_bytes) / delta
        send_speed = (send_bytes - last_send_bytes) / delta

        self._last_net_io_cache = (send_bytes, recv_bytes, tm)
        return recv_speed, send_speed


print(f"steps\t{'date':16}\tread bytes(KiB/sec)\twrite bytes(KiB/sec)\t\
recv bytes(/sec)\tsend bytes(/sec)", end='\t')

steps = 1
# Linux's TASK_COMM_LEN is up to 15.
AGENT_NAME = args.agent[:15]
metrics = []
agent_process_count = 0
io_metrics = IOMetrics()

for proc in psutil.process_iter():
    if proc.name() == AGENT_NAME:
        metric = ProcessMetrics(proc)
        metrics.append(metric)
        CPU = "CPU Usage(%)[{0}#{1}]".format(AGENT_NAME.title(), agent_process_count)
        RSS = "RSS(MB)[{0}#{1}]".format(AGENT_NAME.title(), agent_process_count)
        VMS = "VMS(MB)[{0}#{1}]".format(AGENT_NAME.title(), agent_process_count)
        print(f"{CPU:8}\t{RSS:8}\t{VMS:8}", end="\t")
        agent_process_count = agent_process_count + 1

print("")

while steps <= args.steps:
    now = datetime.now()
    currentTime = now.strftime("%s")

    recv_speed, send_speed = io_metrics.net_io_metrics()
    write_speed, read_speed = io_metrics.disk_io_metrics()
    time_str = now.strftime("%Y/%m/%d %H:%M:%S")
    print(f"{steps}\t{time_str}\t{read_speed /1024 : 16}\t{write_speed /1024 : 16}\t\
    {recv_speed: 16}\t{send_speed: 16}", end='\t')

    for metric in metrics:
        rss, vms = metric.memory_metrics()
        cpu = metric.cpu_percent()
        print(f"{cpu:8}\t{rss /1024/1024 :8}\t{vms /1024/1024 :8}", end='\t')

    print("")
    steps = steps + 1
    while (int(currentTime) >= int(datetime.now().strftime("%s"))):
        time.sleep(0.01)
