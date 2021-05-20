FLUENTD_PACKAGE_NAME ?= "calyptia-fluentd"

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


visualize: visualize-cpu_s visualize-rss_s visualize-vms_s visualize-cpu_w visualize-rss_w visualize-vms_w visualize-read_bytes visualize-write_bytes visualize-recv_bytes visualize-send_bytes

visualize-cpu_s:
	python3 visualize/plot_pandas_Usage.py --resource cpu_s --package-name $(FLUENTD_PACKAGE_NAME)

visualize-rss_s:
	python3 visualize/plot_pandas_Usage.py --resource rss_s --package-name $(FLUENTD_PACKAGE_NAME)

visualize-vms_s:
	python3 visualize/plot_pandas_Usage.py --resource vms_s --package-name $(FLUENTD_PACKAGE_NAME)

visualize-cpu_w:
	python3 visualize/plot_pandas_Usage.py --resource cpu_w --package-name $(FLUENTD_PACKAGE_NAME)

visualize-rss_w:
	python3 visualize/plot_pandas_Usage.py --resource rss_w --package-name $(FLUENTD_PACKAGE_NAME)

visualize-vms_w:
	python3 visualize/plot_pandas_Usage.py --resource vms_w --package-name $(FLUENTD_PACKAGE_NAME)

visualize-read_bytes:
	python3 visualize/plot_pandas_Usage.py --resource read_bytes --package-name $(FLUENTD_PACKAGE_NAME)

visualize-write_bytes:
	python3 visualize/plot_pandas_Usage.py --resource write_bytes --package-name $(FLUENTD_PACKAGE_NAME)

visualize-recv_bytes:
	python3 visualize/plot_pandas_Usage.py --resource recv_bytes --package-name $(FLUENTD_PACKAGE_NAME)

visualize-send_bytes:
	python3 visualize/plot_pandas_Usage.py --resource send_bytes --package-name $(FLUENTD_PACKAGE_NAME)
