#!/usr/bin/env python3

import os
import numpy as  np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import argparse

from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager

parser = argparse.ArgumentParser(description='Visualize data as plot')
parser.add_argument('--resource',
                    choices=['cpu', 'rss', 'vms',
                             'read_bytes', 'write_bytes',
                             'recv_bytes', 'send_bytes'],
                    default='cpu')
parser.add_argument('--package-name', default="td-agent-bit")
args = parser.parse_args()

if args.resource == 'cpu':
    resource_key = "CPU Usage(%)[" + args.package_name.title()[:15] + "#0]"
    xlabel_message = 'flow rate (lines/second)'
    ylabel_message = 'CPU Usage (%)'
    ylimit = 100
    fig_title = 'CPU Usage (Fluent Bit Process) -- ' + args.package_name.title()
    fig_name = args.package_name.title() + '-CPU_usage.png'
    divide_base = -1
elif args.resource == 'rss':
    resource_key = "RSS(MB)[" + args.package_name.title()[:15] + "#0]"
    xlabel_message = 'flow rate (lines/second)'
    ylabel_message = 'RSS Usage (MB) '
    ylimit = 500
    fig_title = 'RSS Usage (Fluent Bit Process) -- ' + args.package_name.title()
    fig_name = args.package_name.title() + '-RSS_usage.png'
    divide_base = -1
elif args.resource == 'vms':
    resource_key = "VMS(MB)[" + args.package_name.title()[:15] + "#0]"
    xlabel_message = 'flow rate (lines/second)'
    ylabel_message = 'VMS Usage (MB)'
    ylimit = 1200
    fig_title = 'VMS Usage (Fluent Bit Process) -- ' + args.package_name.title()
    fig_name = args.package_name.title() + '-VMS_usage.png'
    divide_base = -1
elif args.resource == 'read_bytes':
    resource_key = "read bytes(KiB/sec)"
    xlabel_message = 'flow rate (lines/second)'
    ylabel_message = 'Disk Read Usage (bytes)'
    ylimit = 30000
    fig_title = 'Disk Read Usage -- ' + args.package_name.title()
    fig_name = args.package_name.title() + '-Disk_Read_usage.png'
    divide_base = -1
elif args.resource == 'write_bytes':
    resource_key = "write bytes(KiB/sec)"
    xlabel_message = 'flow rate (lines/second)'
    ylabel_message = 'Disk Write Usage (KiB)'
    ylimit = 150000
    fig_title = 'Disk Write Usage -- ' + args.package_name.title()
    fig_name = args.package_name.title() + '-Disk_Write_usage.png'
    divide_base = -1
elif args.resource == 'recv_bytes':
    resource_key = "recv bytes(/sec)"
    xlabel_message = 'flow rate (lines/second)'
    ylabel_message = 'Receive Usage (Bytes)'
    ylimit = 50000
    fig_title = 'Receive Bytes Usage -- ' + args.package_name.title()
    fig_name = args.package_name.title() + '-Receive_Bytes_usage.png'
    divide_base = -1
elif args.resource == 'send_bytes':
    resource_key = "send bytes(/sec)"
    xlabel_message = 'flow rate (lines/second)'
    ylabel_message = 'Send Usage (Bytes)'
    ylimit = 150000
    fig_title = 'Send Bytes Usage -- ' + args.package_name.title()
    fig_name = args.package_name.title() + '-Send_Bytes_usage.png'
    divide_base = -1

pwd = os.path.dirname(os.path.realpath(__file__))
inventory_file_name = os.path.join(pwd, '..', 'ansible/hosts')
data_loader = DataLoader()
inventory = InventoryManager(loader=data_loader,
                             sources=[inventory_file_name])

collector = inventory.get_groups_dict()['collector'][0]
tfvars = {}
with open("terraform.tfvars") as tfvarfile:
    for line in tfvarfile:
        name, var = line.partition("=")[::2]
        tfvars[name.strip()] = var

print(tfvars)
environment = tfvars["environment"].strip(" \"\n")
if environment == "rhel":
    username = "ec2-user"
else:
    username = "rocky"

print(collector)

sns.set()
sns.set_style('whitegrid')
sns.set_palette('Set3')

base_path = os.path.join(pwd, '..', "ansible", "output", collector, "home", username)
print(base_path)

rate_0    = pd.read_csv(os.path.join(base_path, 'usage-'+ args.package_name + '-0.tsv'), sep='\t', na_values='.')
rate_5000  = pd.read_csv(os.path.join(base_path, 'usage-'+ args.package_name + '-5000.tsv'), sep='\t', na_values='.')
rate_10000 = pd.read_csv(os.path.join(base_path, 'usage-'+ args.package_name + '-10000.tsv'), sep='\t', na_values='.')
rate_100000 = pd.read_csv(os.path.join(base_path, 'usage-'+ args.package_name + '-100000.tsv'), sep='\t', na_values='.')
rate_300000 = pd.read_csv(os.path.join(base_path, 'usage-'+ args.package_name + '-300000.tsv'), sep='\t', na_values='.')

print(resource_key)

df = pd.DataFrame({
    0: rate_0[resource_key],
    5000: rate_5000[resource_key],
    10000: rate_10000[resource_key],
    100000: rate_100000[resource_key],
    300000: rate_300000[resource_key],
})
if divide_base > 1:
    df = df.divide(divide_base)

medians = {0: np.round(df[0].median(), 2),
           5000: np.round(df[5000].median(), 2),
           10000: np.round(df[10000].median(), 2),
           100000: np.round(df[100000].median(), 2),
           300000: np.round(df[300000].median(), 2)}
median_labels = [str(np.round(s, 2)) for s in medians]

print(medians)
df_melt = pd.melt(df)
print(df_melt.head())

fig, ax = plt.subplots(figsize=(8, 6))
ax.set_title(fig_title)
ax.set_ylim(0, ylimit)
plot = sns.boxplot(x='variable', y='value', data=df_melt, showfliers=False, ax=ax, showmeans=True)
plot.set(
    xlabel=xlabel_message,
    ylabel=ylabel_message
)

pos = range(len(medians))
data_range = [0, 5000, 10000, 100000, 300000]
tick = 0
for item in data_range:
    plot.text(tick+0.1, medians[item], medians[item],
              color='w', weight='semibold', size=10, bbox=dict(facecolor='#445A64'))
    tick = tick + 1
sns.stripplot(x='variable', y='value', data=df_melt, jitter=False, color='black', ax=ax
).set(
    xlabel=xlabel_message,
    ylabel=ylabel_message
)

plt.savefig(fig_name)
