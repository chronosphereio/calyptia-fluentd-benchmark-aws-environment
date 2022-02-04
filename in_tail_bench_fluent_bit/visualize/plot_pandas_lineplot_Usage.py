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
args = parser.parse_args()

if args.resource == 'cpu':
    resource_key_format = "CPU Usage(%)[{0}#0]"
    xlabel_message = 'steps'
    ylabel_message = 'CPU Usage (%)'
    ylimit = 100
    fig_title = 'CPU Usage (Fluent Bit Process)'
    fig_name = 'LinePlot-CPU_usage.png'
    divide_base = -1
elif args.resource == 'rss':
    resource_key_format = "RSS(MB)[{0}#0]"
    xlabel_message = 'steps'
    ylabel_message = 'RSS Usage (MB) '
    ylimit = 500
    fig_title = 'RSS Usage (Fluent Bit Process)'
    fig_name = 'LinePlot-RSS_usage.png'
    divide_base = -1
elif args.resource == 'vms':
    resource_key_format = "VMS(MB)[{0}#0]"
    xlabel_message = 'steps'
    ylabel_message = 'VMS Usage (MB)'
    ylimit = 1200
    fig_title = 'VMS Usage (Fluent Bit Process)'
    fig_name = 'LinePlot-VMS_usage.png'
    divide_base = -1
elif args.resource == 'read_bytes':
    resource_key_format = "read bytes(KiB/sec)"
    xlabel_message = 'steps'
    ylabel_message = 'Disk Read Usage (bytes)'
    ylimit = 10000
    fig_title = 'Disk Read Usage'
    fig_name = 'LinePlot-Disk_Read_usage.png'
    divide_base = -1
elif args.resource == 'write_bytes':
    resource_key_format = "write bytes(KiB/sec)"
    xlabel_message = 'steps'
    ylabel_message = 'Disk Write Usage (KiB)'
    ylimit = 30000
    fig_title = 'Disk Write Usage'
    fig_name = 'LinePlot-Disk_Write_usage.png'
    divide_base = -1
elif args.resource == 'recv_bytes':
    resource_key_format = "recv bytes(/sec)"
    xlabel_message = 'steps'
    ylabel_message = 'Receive Usage (Bytes)'
    ylimit = 50000
    fig_title = 'Receive Bytes Usage'
    fig_name = 'LinePlot-Receive_Bytes_usage.png'
    divide_base = -1
elif args.resource == 'send_bytes':
    resource_key_format = "send bytes(/sec)"
    xlabel_message = 'steps'
    ylabel_message = 'Send Usage (Bytes)'
    ylimit = 1500000
    fig_title = 'Send Bytes Usage'
    fig_name = 'LinePlot-Send_Bytes_usage.png'
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

rate_0    = pd.read_csv(os.path.join(base_path, 'usage-td-agent-bit-0.tsv'), sep='\t', na_values='.')
rate_5000  = pd.read_csv(os.path.join(base_path, 'usage-td-agent-bit-5000.tsv'), sep='\t', na_values='.')
rate_10000 = pd.read_csv(os.path.join(base_path, 'usage-td-agent-bit-10000.tsv'), sep='\t', na_values='.')
rate_100000 = pd.read_csv(os.path.join(base_path, 'usage-td-agent-bit-100000.tsv'), sep='\t', na_values='.')
rate_300000 = pd.read_csv(os.path.join(base_path, 'usage-td-agent-bit-300000.tsv'), sep='\t', na_values='.')

df = pd.DataFrame({
    "0 line/sec (baseline) w/ td-agent-bit": rate_0[resource_key_format.format("td-agent-bit".title())],
    "5000 lines/sec w/ td-agent-bit": rate_5000[resource_key_format.format("td-agent-bit".title())],
    "10000 lines/sec w/ td-agent-bit": rate_10000[resource_key_format.format("td-agent-bit".title())],
    "100000 lines/sec w/ td-agent-bit": rate_100000[resource_key_format.format("td-agent-bit".title())],
    "300000 lines/sec w/ td-agent-bit": rate_300000[resource_key_format.format("td-agent-bit".title())],
})
if divide_base > 1:
    df = df_td.divide(divide_base)

fig, ax = plt.subplots(figsize=(8, 6))
ax.set_title(fig_title)
ax.set_ylim(0, ylimit)
palette1 = sns.color_palette('dark', n_colors=5)
plot = sns.lineplot(data=df,
                    ax=ax, lw=0.75, dashes=False, palette=palette1)
plot.set(
    xlabel=xlabel_message,
    ylabel=ylabel_message
)


plt.savefig(fig_name)
