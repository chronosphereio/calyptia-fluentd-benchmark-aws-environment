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
                    choices=['cpu_s', 'rss_s', 'vms_s', 'cpu_w', 'rss_w', 'vms_w',
                             'read_bytes', 'write_bytes',
                             'recv_bytes', 'send_bytes'],
                    default='cpu')
args = parser.parse_args()

if args.resource == 'cpu_s':
    resource_key_format = "CPU Usage(%)[{0}#0]"
    xlabel_message = 'steps'
    ylabel_message = 'CPU Usage (%)'
    ylimit = 100
    fig_title = 'CPU Usage (Supervisor)'
    fig_name = 'LinePlot-CPU_usage_on_supervisor.png'
    divide_base = -1
elif args.resource == 'rss_s':
    resource_key_format = "RSS(MB)[{0}#0]"
    xlabel_message = 'steps'
    ylabel_message = 'RSS Usage (MB) '
    ylimit = 100
    fig_title = 'RSS Usage (Supervisor)'
    fig_name = 'LinePlot-RSS_usage_on_supervisor.png'
    divide_base = -1
elif args.resource == 'vms_s':
    resource_key_format = "VMS(MB)[{0}#0]"
    xlabel_message = 'steps'
    ylabel_message = 'VMS Usage (MB)'
    ylimit = 1200
    fig_title = 'VMS Usage (Supervisor)'
    fig_name = 'LinePlot-VMS_usage_on_supervisor.png'
    divide_base = -1
elif args.resource == 'cpu_w':
    resource_key_format = "CPU Usage(%)[Ruby#0]"
    xlabel_message = 'steps'
    ylabel_message = 'CPU Usage (%)'
    ylimit = 100
    fig_title = 'CPU Usage (Worker)'
    fig_name = 'LinePlot-CPU_usage_on_worker.png'
    divide_base = -1
elif args.resource == 'rss_w':
    resource_key_format = "RSS(MB)[Ruby#0]"
    xlabel_message = 'steps'
    ylabel_message = 'RSS Usage (MB) '
    ylimit = 200
    fig_title = 'RSS Usage (Worker)'
    fig_name = 'LinePlot-RSS_usage_on_worker.png'
    divide_base = -1
elif args.resource == 'vms_w':
    resource_key_format = "VMS(MB)[Ruby#0]"
    xlabel_message = 'steps'
    ylabel_message = 'VMS Usage (MB)'
    ylimit = 1200
    fig_title = 'VMS Usage (Worker)'
    fig_name = 'LinePlot-VMS_usage_on_worker.png'
    divide_base = -1
elif args.resource == 'read_bytes':
    resource_key_format = "read bytes(KiB/sec)"
    xlabel_message = 'steps'
    ylabel_message = 'Disk Read Usage (bytes)'
    ylimit = 2500
    fig_title = 'Disk Read Usage'
    fig_name = 'LinePlot-Disk_Read_usage.png'
    divide_base = -1
elif args.resource == 'write_bytes':
    resource_key_format = "write bytes(KiB/sec)"
    xlabel_message = 'steps'
    ylabel_message = 'Disk Write Usage (KiB)'
    ylimit = 3500
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
    username = "centos"

print(collector)

sns.set()
sns.set_style('whitegrid')
sns.set_palette('Set3')

base_path = os.path.join(pwd, '..', "ansible", "output", collector, "home", username)
print(base_path)

rate_0_calyptia    = pd.read_csv(os.path.join(base_path, 'usage-calyptia-fluentd-0.tsv'), sep='\t', na_values='.')
rate_0_td    = pd.read_csv(os.path.join(base_path, 'usage-td-agent-0.tsv'), sep='\t', na_values='.')
rate_500_calyptia  = pd.read_csv(os.path.join(base_path, 'usage-calyptia-fluentd-500.tsv'), sep='\t', na_values='.')
rate_500_td  = pd.read_csv(os.path.join(base_path, 'usage-td-agent-500.tsv'), sep='\t', na_values='.')
rate_1000_calyptia = pd.read_csv(os.path.join(base_path, 'usage-calyptia-fluentd-1000.tsv'), sep='\t', na_values='.')
rate_1000_td = pd.read_csv(os.path.join(base_path, 'usage-td-agent-1000.tsv'), sep='\t', na_values='.')
rate_1500_calyptia = pd.read_csv(os.path.join(base_path, 'usage-calyptia-fluentd-1500.tsv'), sep='\t', na_values='.')
rate_1500_td = pd.read_csv(os.path.join(base_path, 'usage-td-agent-1500.tsv'), sep='\t', na_values='.')

df_td = pd.DataFrame({
    "0 line/sec (baseline) w/ td-agent": rate_0_td[resource_key_format.format("td-agent".title())],
    "500 lines/sec w/ td-agent": rate_500_td[resource_key_format.format("td-agent".title())],
    "1000 lines/sec w/ td-agent": rate_1000_td[resource_key_format.format("td-agent".title())],
    "1500 lines/sec w/ td-agent": rate_1500_td[resource_key_format.format("td-agent".title())],
})
if divide_base > 1:
    df_td = df_td.divide(divide_base)

df_calyptia = pd.DataFrame({
    "0 line/sec (baseline) w/ calyptia-fluentd": rate_0_calyptia[resource_key_format.format("calyptia-fluentd"[:15].title())],
    "500 lines/sec w/ calyptia-fluentd": rate_500_calyptia[resource_key_format.format("calyptia-fluentd"[:15].title())],
    "1000 lines/sec w/ calyptia-fluentd": rate_1000_calyptia[resource_key_format.format("calyptia-fluentd"[:15].title())],
    "1500 lines/sec w/ calyptia-fluentd": rate_1500_calyptia[resource_key_format.format("calyptia-fluentd"[:15].title())],
})
if divide_base > 1:
    df_calyptia = df_calyptia.divide(divide_base)

fig, ax = plt.subplots(figsize=(8, 6))
ax.set_title(fig_title)
ax.set_ylim(0, ylimit)
palette1 = sns.color_palette('dark', n_colors=4)
plot = sns.lineplot(data=df_td,
                    ax=ax, lw=0.75, dashes=False, palette=palette1)
plot.set(
    xlabel=xlabel_message,
    ylabel=ylabel_message
)
palette2 = sns.color_palette('pastel', n_colors=4)
plot2 = sns.lineplot(data=df_calyptia,
                     ax=ax, lw=0.75, dashes=False, palette=palette2)
plot2.set(
    xlabel=xlabel_message,
    ylabel=ylabel_message
)


plt.savefig(fig_name)
