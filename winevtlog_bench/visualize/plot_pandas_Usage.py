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
    xlabel_message = 'message length (bytes)'
    ylabel_message = 'CPU Usage (%)'
    ylimit = 100
    fig_title = 'CPU Usage (Supervisor)'
    fig_name = 'CPU_usage_on_supervisor.png'
    divide_base = -1
elif args.resource == 'cpu_w':
    resource_key = '\\\\FLUENTD-WINSERV\\Process(ruby#1)\\% Processor Time'
    xlabel_message = 'message length (bytes)'
    ylabel_message = 'CPU Usage (%)'
    ylimit = 100
    fig_title = 'CPU Usage (Worker)'
    fig_name = 'CPU_usage_on_worker.png'
    divide_base = -1
elif args.resource == 'private_bytes_s':
    resource_key = '\\\\FLUENTD-WINSERV\\Process(ruby)\\Private Bytes'
    xlabel_message = 'message length (bytes)'
    ylabel_message = 'Private Bytes Usage (MB)'
    ylimit = 200
    fig_title = 'Private Bytes Usage (Supervisor)'
    fig_name = 'Private_Bytes_usage_on_supervisor.png'
    divide_base = 1024*1024
elif args.resource == 'private_bytes_w':
    resource_key = '\\\\FLUENTD-WINSERV\\Process(ruby#1)\\Private Bytes'
    xlabel_message = 'message length (bytes)'
    ylabel_message = 'Private Bytes (MB)'
    ylimit = 200
    fig_title = 'Private Bytes Usage (Worker)'
    fig_name = 'Private_Bytes_usage_on_worker.png'
    divide_base = 1024*1024
elif args.resource == 'working_set_s':
    resource_key = '\\\\FLUENTD-WINSERV\\Process(ruby)\\Working Set'
    xlabel_message = 'message length (bytes)'
    ylabel_message = 'Working Set (MB)'
    ylimit = 100
    fig_title = 'Working Set Usage (Supervisor)'
    fig_name = 'Working_Set_usage_on_supervisor.png'
    divide_base = 1024*1024
elif args.resource == 'working_set_w':
    resource_key = '\\\\FLUENTD-WINSERV\\Process(ruby#1)\\Working Set'
    xlabel_message = 'message length (bytes)'
    ylabel_message = 'Working Set (MB)'
    ylimit = 100
    fig_title = 'Working Set Usage (Worker)'
    fig_name = 'Working_Set_usage_on_worker.png'
    divide_base = 1024*1024
elif args.resource == 'sent_bytes':
    resource_key = '\\\\FLUENTD-WINSERV\\Network Interface(AWS PV Network Device _0)\\Bytes Sent/sec'
    xlabel_message = 'message length (bytes)'
    ylabel_message = 'Bytes Sent (KiB/sec)'
    ylimit = 3500
    fig_title = 'Bytes Sent Usage'
    fig_name = 'Bytes_Sent_usage.png'
    divide_base = 1024
elif args.resource == 'received_bytes':
    resource_key = '\\\\FLUENTD-WINSERV\\Network Interface(AWS PV Network Device _0)\\Bytes Received/sec'
    xlabel_message = 'message length (bytes)'
    ylabel_message = 'Bytes Received (KiB/sec)'
    ylimit = 2000
    fig_title = 'Bytes Received Usage'
    fig_name = 'Bytes_Received_usage.png'
    divide_base = 1024
elif args.resource == 'disk_reads':
    resource_key = '\\\\FLUENTD-WINSERV\\PhysicalDisk(_Total)\\Disk Reads/sec'
    xlabel_message = 'message length (bytes)'
    ylabel_message = 'Disk Read (bytes/sec)'
    ylimit = 1000
    fig_title = 'Disk Read Usage'
    fig_name = 'Disk_Read_usage.png'
    divide_base = -1
elif args.resource == 'disk_writes':
    resource_key = '\\\\FLUENTD-WINSERV\\PhysicalDisk(_Total)\\Disk Writes/sec'
    xlabel_message = 'message length (bytes)'
    ylabel_message = 'Disk Write (bytes/sec)'
    ylimit = 1000
    fig_title = 'Disk Write Usage'
    fig_name = 'Disk_Write_usage.png'
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

length_512 = pd.read_csv(os.path.join(base_path, '512-resource-usage.csv'), sep=',', na_values='.')
length_1024 = pd.read_csv(os.path.join(base_path, '1024-resource-usage.csv'), sep=',', na_values='.')
length_2048 = pd.read_csv(os.path.join(base_path, '2048-resource-usage.csv'), sep=',', na_values='.')

df = pd.DataFrame({
    512: length_512[resource_key],
    1024: length_1024[resource_key],
    2048: length_2048[resource_key],
})
if divide_base > 1:
    df = df.divide(divide_base)

medians = {512: np.round(df[512].median(), 2),
           1024: np.round(df[1024].median(), 2),
           2048: np.round(df[2048].median(), 2)}
median_labels = [str(np.round(s, 2)) for s in medians]

print(medians)
df_melt = pd.melt(df)
print(df_melt.head())

fig = plt.figure()
plt.title(fig_title)
f, ax = plt.subplots()
ax.set_ylim(0, ylimit)
plot = sns.boxplot(x='variable', y='value', data=df_melt, showfliers=False,
                   ax=ax, showmeans=True)
plot.set(
    xlabel=xlabel_message,
    ylabel=ylabel_message
)

pos = range(len(medians))
data_range = [512, 1024, 2048]
tick = 0
for item in data_range:
    plot.text(tick+0.1, medians[item], medians[item],
              color='w', weight='semibold', size=10,
              bbox=dict(facecolor='#445A64'))
    tick = tick + 1
sns.stripplot(x='variable', y='value', data=df_melt,
              jitter=False, color='black', ax=ax,
).set(
    xlabel=xlabel_message,
    ylabel=ylabel_message
)

plt.savefig(fig_name)
