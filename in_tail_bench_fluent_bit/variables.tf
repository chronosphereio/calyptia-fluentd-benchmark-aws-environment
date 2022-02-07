variable "prefix" {
  default = "fluent-bit"
}

variable "provider-region" {}
variable "secret-access-key" {}
variable "secret-key" {}
variable "availability-zone" {}
variable "ssh-private-key-path" {}
variable "environment" {}
variable "instance_type" {
  default = "t2.medium"

  validation {
    condition     = contains(["t2.medium", "i3en.large"], var.instance_type)
    error_message = "Valid values for var: instance_type are (t2.medium, i3en.large)."
  }
}