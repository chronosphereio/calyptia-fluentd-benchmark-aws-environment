Fluentd Benchmark Azure Environment with Terraform
===

## Prerequisites

* Terraform 0.12+
* Ansible 2.9+

## Setup

 1. Prepare RSA public key and put it into `azure_key/id_rsa_azure.pub`.
 2. Prepare env.sh and fill `ARM_` prefixed environment variables with your credentials.
 3. Specify user-defined variables in `terraform.tfvars` which can copy from `terraform.tfvars.sample`.

## Usage

```
$ terraform plan
```

and then,

```
$ terraform apply
```