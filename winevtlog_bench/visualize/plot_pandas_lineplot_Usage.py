#!/usr/bin/env python3

import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import argparse

from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager

parser = argparse.ArgumentParser(description='Visualize data as plot')
parser.add_argument('--resource',
                    choices=['cpu_s', 'cpu_w',
                             'private_bytes_s', 'private_bytes_w',
                             'working_set_s', 'working_set_w',
                             'sent_bytes', 'received_bytes',
                             'disk_reads', 'disk_writes'],
                    default='cpu')
parser.add_argument('--base-path', default='')
args = parser.parse_args()

if args.resource == 'cpu_s':
    resource_key = '\\\\FLUENTD-WINSERV\\Process(ruby)\\% Processor Time'
    xlabel_message = 'steps'
    ylabel_message = 'CPU Usage (%)'
    ylimit = 100
    fig_title = 'CPU Usage (Supervisor)'
    fig_name = 'LinePlot-CPU_usage_on_supervisor.png'
    divide_base = -1
elif args.resource == 'cpu_w':
    resource_key = '\\\\FLUENTD-WINSERV\\Process(ruby#1)\\% Processor Time'
    xlabel_message = 'steps'
    ylabel_message = 'CPU Usage (%)'
    ylimit = 100
    fig_title = 'CPU Usage (Worker)'
    fig_name = 'LinePlot-CPU_usage_on_worker.png'
    divide_base = -1
elif args.resource == 'private_bytes_s':
    resource_key = '\\\\FLUENTD-WINSERV\\Process(ruby)\\Private Bytes'
    xlabel_message = 'steps'
    ylabel_message = 'Private Bytes Usage (MB)'
    ylimit = 200
    fig_title = 'Private Bytes Usage (Supervisor)'
    fig_name = 'LinePlot-Private_Bytes_usage_on_supervisor.png'
    divide_base = 1024*1024
elif args.resource == 'private_bytes_w':
    resource_key = '\\\\FLUENTD-WINSERV\\Process(ruby#1)\\Private Bytes'
    xlabel_message = 'steps'
    ylabel_message = 'Private Bytes (MB)'
    ylimit = 200
    fig_title = 'Private Bytes Usage (Worker)'
    fig_name = 'LinePlot-Private_Bytes_usage_on_worker.png'
    divide_base = 1024*1024
elif args.resource == 'working_set_s':
    resource_key = '\\\\FLUENTD-WINSERV\\Process(ruby)\\Working Set'
    xlabel_message = 'steps'
    ylabel_message = 'Working Set (MB)'
    ylimit = 100
    fig_title = 'Working Set Usage (Supervisor)'
    fig_name = 'LinePlot-Working_Set_usage_on_supervisor.png'
    divide_base = 1024*1024
elif args.resource == 'working_set_w':
    resource_key = '\\\\FLUENTD-WINSERV\\Process(ruby#1)\\Working Set'
    xlabel_message = 'steps'
    ylabel_message = 'Working Set (MB)'
    ylimit = 100
    fig_title = 'Working Set Usage (Worker)'
    fig_name = 'LinePlot-Working_Set_usage_on_worker.png'
    divide_base = 1024*1024
elif args.resource == 'sent_bytes':
    resource_key = '\\\\FLUENTD-WINSERV\\Network Interface(AWS PV Network Device _0)\\Bytes Sent/sec'
    xlabel_message = 'steps'
    ylabel_message = 'Bytes Sent (KiB/sec)'
    ylimit = 3500
    fig_title = 'Bytes Sent Usage'
    fig_name = 'LinePlot-Bytes_Sent_usage.png'
    divide_base = 1024
elif args.resource == 'received_bytes':
    resource_key = '\\\\FLUENTD-WINSERV\\Network Interface(AWS PV Network Device _0)\\Bytes Received/sec'
    xlabel_message = 'steps'
    ylabel_message = 'Bytes Received (KiB/sec)'
    ylimit = 2000
    fig_title = 'Bytes Received Usage'
    fig_name = 'LinePlot-Bytes_Received_usage.png'
    divide_base = 1024
elif args.resource == 'disk_reads':
    resource_key = '\\\\FLUENTD-WINSERV\\PhysicalDisk(_Total)\\Disk Reads/sec'
    xlabel_message = 'steps'
    ylabel_message = 'Disk Read (bytes/sec)'
    ylimit = 1000
    fig_title = 'Disk Read Usage'
    fig_name = 'LinePlot-Disk_Read_usage.png'
    divide_base = -1
elif args.resource == 'disk_writes':
    resource_key = '\\\\FLUENTD-WINSERV\\PhysicalDisk(_Total)\\Disk Writes/sec'
    xlabel_message = 'steps'
    ylabel_message = 'Disk Write (bytes/sec)'
    ylimit = 1000
    fig_title = 'Disk Write Usage'
    fig_name = 'LinePlot-Disk_Write_usage.png'
    divide_base = -1


sns.set()
sns.set_style('whitegrid')
sns.set_palette('Set3')

if args.base_path == '':
    pwd = os.path.dirname(os.path.realpath(__file__))
    inventory_file_name = os.path.join(pwd, '..', 'ansible/hosts')
    data_loader = DataLoader()
    inventory = InventoryManager(loader=data_loader,
                                 sources=[inventory_file_name])

    collector = inventory.get_groups_dict()['windows'][0]
    print(collector)
    base_path = os.path.join(pwd, '..', "ansible", "output", collector, "C:", "tools")
else:
    base_path = args.base_path
print(base_path)

length_512_calyptia = pd.read_csv(os.path.join(base_path, '512-calyptia-fluentd-resource-usage.csv'), sep=',', na_values='.')
length_512_td = pd.read_csv(os.path.join(base_path, '512-td-agent-resource-usage.csv'), sep=',', na_values='.')
length_1024_calyptia = pd.read_csv(os.path.join(base_path, '1024-calyptia-fluentd-resource-usage.csv'), sep=',', na_values='.')
length_1024_td = pd.read_csv(os.path.join(base_path, '1024-td-agent-resource-usage.csv'), sep=',', na_values='.')
length_2048_calyptia = pd.read_csv(os.path.join(base_path, '2048-calyptia-fluentd-resource-usage.csv'), sep=',', na_values='.')
length_2048_td = pd.read_csv(os.path.join(base_path, '2048-td-agent-resource-usage.csv'), sep=',', na_values='.')

df_td = pd.DataFrame({
    "512 bytes w/ td-agent": length_512_td[resource_key],
    "1024 bytes w/ td-agent": length_1024_td[resource_key],
    "2048 bytes w/ td-agent": length_2048_td[resource_key],
})
if divide_base > 1:
    df_td = df_td.divide(divide_base)

df_calyptia = pd.DataFrame({
    "512 bytes w/ calyptia-fluentd": length_512_calyptia[resource_key],
    "1024 bytes w/ calyptia-fluentd": length_1024_calyptia[resource_key],
    "2048 bytes w/ calyptia-fluentd": length_2048_calyptia[resource_key],
})
if divide_base > 1:
    df_calyptia = df_calyptia.divide(divide_base)

fig, ax = plt.subplots(figsize=(8, 6))
ax.set_title(fig_title)
ax.set_ylim(0, ylimit)
palette1 = sns.color_palette('dark', n_colors=3)
plot = sns.lineplot(data=df_td,
                    ax=ax, lw=0.75, dashes=False, palette=palette1)
plot.set(
    xlabel=xlabel_message,
    ylabel=ylabel_message
)
palette2 = sns.color_palette('pastel', n_colors=3)
plot2 = sns.lineplot(data=df_calyptia,
                     ax=ax, lw=0.75, dashes=False, palette=palette2)
plot2.set(
    xlabel=xlabel_message,
    ylabel=ylabel_message
)

plt.savefig(fig_name)
