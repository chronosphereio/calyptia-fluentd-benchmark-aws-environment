Calyptia Fluentd Benchmark AWS Environment with Terraform
===

[![Lint terraform and ansible recipe on Ubuntu](https://github.com/calyptia/calyptia-fluentd-benchmark-aws-environment/actions/workflows/terraform-lint.yml/badge.svg?branch=calyptia-bench)](https://github.com/calyptia/calyptia-fluentd-benchmark-aws-environment/actions/workflows/terraform-lint.yml)

## Prerequisites

* Terraform 0.13+
* Python3 3.6+
* Ansible 3.0+
* make
* AWS access key which can manage EC2 instances

## Setup

 1. Prepare RSA public key and put it into `aws_key/id_rsa_aws.pub`.
 2. Change directory to target environments(winevtlog_bench/in_tail_bench).
 3. Specify user-defined variables in `terraform.tfvars` which can be copied from `terraform.tfvars.sample` and fill them for each environment (winevtlog\_bench, in\_tail\_bench).

## Usage

### Prepare Python libraries

```
$ pip install -r requirements.txt
```

Or, creating virtual environment wirth venv

```
$ python3 -m venv management
```

And then,

```
$ source management/bin/activate
$ pip install -r requirements.txt
```

### Windows EventLog Scenario Benchmark

See [README.md](winevtlog_bench/README.md) about details.

### in\_tail Scenario Benchmark

See [README.md](in_tail_bench/README.md) about details.


### in\_syslog Scenario Benchmark

See [README.md](in_syslog_bench/README.md) about details.


### in\_sample_systemlog Scenario Benchmark

See [README.md](in_sample_systemlog/README.md) about details.


## License

[MIT](LICENSE).
