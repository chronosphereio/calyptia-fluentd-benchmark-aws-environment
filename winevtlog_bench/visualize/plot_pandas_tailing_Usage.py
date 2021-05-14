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
    ylimit = 150
    fig_title = 'Private Bytes Usage (Supervisor)'
    fig_name = 'Private_Bytes_usage_on_supervisor.png'
    divide_base = 1024*1024
elif args.resource == 'private_bytes_w':
    resource_key = '\\\\FLUENTD-WINSERV\\Process(ruby#1)\\Private Bytes'
    xlabel_message = 'message length (bytes)'
    ylabel_message = 'Private Bytes (MB)'
    ylimit = 150
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
    ylimit = 2000
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

sns.set(font_scale = 1.5)
sns.set_style('whitegrid')
sns.set_palette('Set3')

events_50_appends_50 = pd.read_csv(os.path.join(base_path, '50events-50lines-resource-usage.csv'), sep=',', na_values='.', skipfooter=2, engine='python')
events_50_appends_1200 = pd.read_csv(os.path.join(base_path, '50events-1200lines-resource-usage.csv'), sep=',', na_values='.', skipfooter=2, engine='python')
events_50_appends_1500 = pd.read_csv(os.path.join(base_path, '50events-1500lines-resource-usage.csv'), sep=',', na_values='.', skipfooter=2, engine='python')
events_50_appends_2000 = pd.read_csv(os.path.join(base_path, '50events-2000lines-resource-usage.csv'), sep=',', na_values='.', skipfooter=2, engine='python')
events_80_appends_1200 = pd.read_csv(os.path.join(base_path, '80events-1200lines-resource-usage.csv'), sep=',', na_values='.', skipfooter=2, engine='python')
events_80_appends_1500 = pd.read_csv(os.path.join(base_path, '80events-1500lines-resource-usage.csv'), sep=',', na_values='.', skipfooter=2, engine='python')
events_100_appends_100 = pd.read_csv(os.path.join(base_path, '100events-100lines-resource-usage.csv'), sep=',', na_values='.', skipfooter=2, engine='python')
events_100_appends_200 = pd.read_csv(os.path.join(base_path, '100events-200lines-resource-usage.csv'), sep=',', na_values='.', skipfooter=2, engine='python')
events_100_appends_400 = pd.read_csv(os.path.join(base_path, '100events-400lines-resource-usage.csv'), sep=',', na_values='.', skipfooter=2, engine='python')
events_100_appends_800 = pd.read_csv(os.path.join(base_path, '100events-800lines-resource-usage.csv'), sep=',', na_values='.', skipfooter=2, engine='python')
events_100_appends_1000 = pd.read_csv(os.path.join(base_path, '100events-1000lines-resource-usage.csv'), sep=',', na_values='.', skipfooter=2, engine='python')
events_120_appends_200 = pd.read_csv(os.path.join(base_path, '120events-200lines-resource-usage.csv'), sep=',', na_values='.', skipfooter=2, engine='python')
events_120_appends_400 = pd.read_csv(os.path.join(base_path, '120events-400lines-resource-usage.csv'), sep=',', na_values='.', skipfooter=2, engine='python')
events_120_appends_800 = pd.read_csv(os.path.join(base_path, '120events-800lines-resource-usage.csv'), sep=',', na_values='.', skipfooter=2, engine='python')
events_140_appends_200 = pd.read_csv(os.path.join(base_path, '140events-200lines-resource-usage.csv'), sep=',', na_values='.', skipfooter=2, engine='python')
events_140_appends_400 = pd.read_csv(os.path.join(base_path, '140events-400lines-resource-usage.csv'), sep=',', na_values='.', skipfooter=2, engine='python')
events_140_appends_600 = pd.read_csv(os.path.join(base_path, '140events-600lines-resource-usage.csv'), sep=',', na_values='.', skipfooter=2, engine='python')
events_150_appends_200 = pd.read_csv(os.path.join(base_path, '150events-200lines-resource-usage.csv'), sep=',', na_values='.', skipfooter=2, engine='python')
events_150_appends_300 = pd.read_csv(os.path.join(base_path, '150events-300lines-resource-usage.csv'), sep=',', na_values='.', skipfooter=2, engine='python')
print(events_50_appends_50)
df = pd.DataFrame({
    "50events_50lines":    events_50_appends_50[resource_key],
    "50events_1200lines":  events_50_appends_1200[resource_key],
    "50events_1500lines":  events_50_appends_1500[resource_key],
    "50events_2000lines":  events_50_appends_2000[resource_key],
    "80events_1200lines":  events_80_appends_1200[resource_key],
    "80events_1500lines":  events_80_appends_1500[resource_key],
    "100events_100lines":  events_100_appends_100[resource_key],
    "100events_200lines":  events_100_appends_200[resource_key],
    "100events_400lines":  events_100_appends_400[resource_key],
    "100events_800lines":  events_100_appends_800[resource_key],
    "100events_1000lines": events_100_appends_1000[resource_key],
    "120events_200lines":  events_120_appends_200[resource_key],
    "120events_400lines":  events_120_appends_400[resource_key],
    "120events_800lines":  events_120_appends_800[resource_key],
    "140events_200lines":  events_140_appends_200[resource_key],
    "140events_400lines":  events_140_appends_400[resource_key],
    "140events_600lines":  events_140_appends_600[resource_key],
    "150events_200lines":  events_150_appends_200[resource_key],
    "150events_300lines":  events_150_appends_300[resource_key],
})
if divide_base > 1:
    df = df.divide(divide_base)

medians = {"50events_50lines":    np.round(df["50events_50lines"].median(), 2),
           "50events_1200lines":  np.round(df["50events_1200lines"].median(), 2),
           "50events_1500lines":  np.round(df["50events_1500lines"].median(), 2),
           "50events_2000lines":  np.round(df["50events_2000lines"].median(), 2),
           "80events_1200lines":  np.round(df["80events_1200lines"].median(), 2),
           "80events_1500lines":  np.round(df["80events_1500lines"].median(), 2),
           "100events_100lines":  np.round(df["100events_100lines"].median(), 2),
           "100events_200lines":  np.round(df["100events_200lines"].median(), 2),
           "100events_400lines":  np.round(df["100events_400lines"].median(), 2),
           "100events_800lines":  np.round(df["100events_800lines"].median(), 2),
           "100events_1000lines": np.round(df["100events_1000lines"].median(), 2),
           "120events_200lines":  np.round(df["120events_200lines"].median(), 2),
           "120events_400lines":  np.round(df["120events_400lines"].median(), 2),
           "120events_800lines":  np.round(df["120events_800lines"].median(), 2),
           "140events_200lines":  np.round(df["140events_200lines"].median(), 2),
           "140events_400lines":  np.round(df["140events_400lines"].median(), 2),
           "140events_600lines":  np.round(df["140events_600lines"].median(), 2),
           "150events_200lines":  np.round(df["150events_200lines"].median(), 2),
           "150events_300lines":  np.round(df["150events_300lines"].median(), 2)}
median_labels = [str(s) for s in medians]

print(medians)
df_melt = pd.melt(df)
print(df_melt.head())

fig = plt.figure(figsize=(23, 12))
plt.title(fig_title)

f, ax = plt.subplots(figsize=(23, 12))
ax.set_ylim(0, ylimit)
plot = sns.boxplot(x='variable', y='value', data=df_melt, showfliers=False,
                   ax=ax, showmeans=True)
plot.set(
    xlabel=xlabel_message,
    ylabel=ylabel_message
)
plot.set_xticklabels(plot.get_xticklabels(), rotation=30, horizontalalignment='right')

pos = range(len(medians))
data_range = [
    "50events_50lines",   "50events_1200lines", "50events_1500lines", "50events_2000lines",
    "80events_1200lines", "80events_1500lines",
    "100events_100lines", "100events_200lines", "100events_400lines",
    "100events_800lines", "100events_1000lines",
    "120events_200lines", "120events_400lines", "120events_800lines",
    "140events_200lines", "140events_400lines", "140events_600lines",
    "150events_200lines", "150events_300lines"
]
tick = 0
for item in data_range:
    plot.text(tick+0.1, medians[item], medians[item],
              color='w', weight='semibold', size=12,
              bbox=dict(facecolor='#445A64'))
    tick = tick + 1
chart = sns.stripplot(x='variable', y='value', data=df_melt,
              jitter=False, color='black', ax=ax)
chart.set(
    xlabel=xlabel_message,
    ylabel=ylabel_message
)
chart.set_xticklabels(chart.get_xticklabels(), rotation=30, horizontalalignment='right')

plt.savefig(fig_name)
