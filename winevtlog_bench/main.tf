# definition provider
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }

    local = {
      version = "~> 2.1"
    }

    null = {
      version = "~> 3.1"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "${var.provider-region}"
  access_key = "${var.secret-access-key}"
  secret_key = "${var.secret-key}"
}

provider "local" {}
provider "null" {}
