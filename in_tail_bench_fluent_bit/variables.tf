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
    condition     = contains(["t2.medium", "i3en.large", "i3en.2xlarge"], var.instance_type)
    error_message = "Valid values for var: instance_type are (t2.medium, i3en.large, i3en.2xlarge)."
  }
}
variable "extra_block_devices" {
  type = list
  default = [
    { device_name = "/dev/xvdf", volume_type = "gp3", volume_size = "100" },
  ]
}
