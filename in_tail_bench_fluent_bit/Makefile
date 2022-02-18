FLUENT_BIT_PACKAGE_NAME ?= "fluent-bit"

.PHONY: all

all: apply provision

clean:
	terraform destroy -auto-approve

apply:
	terraform apply -auto-approve

provision: collector-provision aggregator-provision

plan:
	terraform plan

collector-provision:
	ansible-playbook -i ./ansible/hosts ./ansible/collector.yml

aggregator-provision:
	ansible-playbook -i ./ansible/hosts ./ansible/aggregator.yml

tail-bench:
	ansible-playbook -i ./ansible/hosts ./ansible/tail-bench.yml

visualize-line: visualize-line-cpu visualize-line-cpu-total visualize-line-vms visualize-line-rss


visualize-line-cpu:
	python3 visualize/plot_pandas_lineplot_Usage.py --resource cpu

visualize-line-cpu-total:
	python3 visualize/plot_pandas_lineplot_Usage.py --resource cpu-total

visualize-line-vms:
	python3 visualize/plot_pandas_lineplot_Usage.py --resource vms

visualize-line-rss:
	python3 visualize/plot_pandas_lineplot_Usage.py --resource rss

visualize: visualize-cpu visualize-rss visualize-vms visualize-read_bytes visualize-write_bytes visualize-recv_bytes visualize-send_bytes

visualize-cpu:
	python3 visualize/plot_pandas_Usage.py --resource cpu --package-name $(FLUENT_BIT_PACKAGE_NAME)

visualize-vms:
	python3 visualize/plot_pandas_Usage.py --resource vms --package-name $(FLUENT_BIT_PACKAGE_NAME)

visualize-rss:
	python3 visualize/plot_pandas_Usage.py --resource rss --package-name $(FLUENT_BIT_PACKAGE_NAME)

visualize-read_bytes:
	python3 visualize/plot_pandas_Usage.py --resource read_bytes --package-name $(FLUENT_BIT_PACKAGE_NAME)

visualize-write_bytes:
	python3 visualize/plot_pandas_Usage.py --resource write_bytes --package-name $(FLUENT_BIT_PACKAGE_NAME)

visualize-recv_bytes:
	python3 visualize/plot_pandas_Usage.py --resource recv_bytes --package-name $(FLUENT_BIT_PACKAGE_NAME)

visualize-send_bytes:
	python3 visualize/plot_pandas_Usage.py --resource send_bytes --package-name $(FLUENT_BIT_PACKAGE_NAME)
