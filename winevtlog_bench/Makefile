FLUENTD_PACKAGE_NAME ?= "calyptia-fluentd"

.PHONY: all

all: apply provision

clean:
	terraform destroy -auto-approve

apply:
	terraform apply -auto-approve

plan:
	terraform plan

provision: windows-provision aggregator-provision

windows-provision:
	ansible-playbook -i ./ansible/hosts ./ansible/windows.yml --extra-vars "local_package=no"

aggregator-provision:
	ansible-playbook -i ./ansible/hosts ./ansible/aggregator.yml

# This target is used for testing modified version of local package
local-package-provision:
	@if [ "$(FLUENTD_LOCAL_PACKAGE)" = "" ]; then \
		echo "Set FLUENTD_LOCAL_PACKAGE to use modified version of installer"; \
		echo "e.g. export FLUENTD_LOCAL_PACKAGE=./config/calyptia-fluentd-1.0.50-x64.msi"; \
		exit 1; \
	fi
	ansible-playbook -i ./ansible/hosts ./ansible/windows.yml --extra-vars "local_package=$(FLUENTD_LOCAL_PACKAGE)"
	ansible-playbook -i ./ansible/hosts ./ansible/aggregator.yml

windows-bench:
	ansible-playbook -i ./ansible/hosts ./ansible/windows-bench.yml

visualize-line: visualize-line-cpu_s visualize-line-cpu_w visualize-line-private_bytes_s visualize-line-private_bytes_w visualize-line-working_set_s visualize-line-working_set_w


visualize-line-cpu_s:
	python3 visualize/plot_pandas_lineplot_Usage.py --resource cpu_s

visualize-line-cpu_w:
	python3 visualize/plot_pandas_lineplot_Usage.py --resource cpu_w

visualize-line-private_bytes_s:
	python3 visualize/plot_pandas_lineplot_Usage.py --resource private_bytes_s

visualize-line-private_bytes_w:
	python3 visualize/plot_pandas_lineplot_Usage.py --resource private_bytes_w

visualize-line-working_set_s:
	python3 visualize/plot_pandas_lineplot_Usage.py --resource working_set_s

visualize-line-working_set_w:
	python3 visualize/plot_pandas_lineplot_Usage.py --resource working_set_w

visualize: visualize-cpu_s visualize-cpu_w visualize-private_bytes_s visualize-private_bytes_w visualize-working_set_s visualize-working_set_w visualize-sent_bytes visualize-received_bytes visualize-disk_reads visualize-disk_writes

visualize-cpu_s:
	python3 visualize/plot_pandas_Usage.py --resource cpu_s --package-name $(FLUENTD_PACKAGE_NAME)

visualize-cpu_w:
	python3 visualize/plot_pandas_Usage.py --resource cpu_w --package-name $(FLUENTD_PACKAGE_NAME)

visualize-private_bytes_s:
	python3 visualize/plot_pandas_Usage.py --resource private_bytes_s --package-name $(FLUENTD_PACKAGE_NAME)

visualize-private_bytes_w:
	python3 visualize/plot_pandas_Usage.py --resource private_bytes_w --package-name $(FLUENTD_PACKAGE_NAME)

visualize-working_set_s:
	python3 visualize/plot_pandas_Usage.py --resource working_set_s --package-name $(FLUENTD_PACKAGE_NAME)

visualize-working_set_w:
	python3 visualize/plot_pandas_Usage.py --resource working_set_w --package-name $(FLUENTD_PACKAGE_NAME)

visualize-sent_bytes:
	python3 visualize/plot_pandas_Usage.py --resource sent_bytes --package-name $(FLUENTD_PACKAGE_NAME)

visualize-received_bytes:
	python3 visualize/plot_pandas_Usage.py --resource received_bytes --package-name $(FLUENTD_PACKAGE_NAME)

visualize-disk_reads:
	python3 visualize/plot_pandas_Usage.py --resource disk_reads --package-name $(FLUENTD_PACKAGE_NAME)

visualize-disk_writes:
	python3 visualize/plot_pandas_Usage.py --resource disk_writes --package-name $(FLUENTD_PACKAGE_NAME)

windows-bench-with-tailing:
	ansible-playbook -i ./ansible/hosts ./ansible/windows-bench-with-tailing.yml

visualize-tailing: visualize-tailing-cpu_s visualize-tailing-cpu_w visualize-tailing-private_bytes_s visualize-tailing-private_bytes_w visualize-tailing-working_set_s visualize-tailing-working_set_w visualize-tailing-sent_bytes visualize-tailing-received_bytes visualize-tailing-disk_reads visualize-tailing-disk_writes

visualize-tailing-cpu_s:
	python3 visualize/plot_pandas_tailing_Usage.py --resource cpu_s

visualize-tailing-cpu_w:
	python3 visualize/plot_pandas_tailing_Usage.py --resource cpu_w

visualize-tailing-private_bytes_s:
	python3 visualize/plot_pandas_tailing_Usage.py --resource private_bytes_s

visualize-tailing-private_bytes_w:
	python3 visualize/plot_pandas_tailing_Usage.py --resource private_bytes_w

visualize-tailing-working_set_s:
	python3 visualize/plot_pandas_tailing_Usage.py --resource working_set_s

visualize-tailing-working_set_w:
	python3 visualize/plot_pandas_tailing_Usage.py --resource working_set_w

visualize-tailing-sent_bytes:
	python3 visualize/plot_pandas_tailing_Usage.py --resource sent_bytes

visualize-tailing-received_bytes:
	python3 visualize/plot_pandas_tailing_Usage.py --resource received_bytes

visualize-tailing-disk_reads:
	python3 visualize/plot_pandas_tailing_Usage.py --resource disk_reads

visualize-tailing-disk_writes:
	python3 visualize/plot_pandas_tailing_Usage.py --resource disk_writes
