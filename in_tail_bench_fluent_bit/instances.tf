data "aws_ami" "rocky8" {
  most_recent = true

  filter {
    name   = "name"
    values = ["Rocky-8*"]
  }

  filter {
    name   = "architecture"
    values = ["x86_64"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["792107900819"]
}

data "aws_ami" "rhel8" {
  most_recent = true
  name_regex  = "^RHEL-8.5.0_HVM-"
  owners      = ["309956199498"] # Red Hat's account ID.

  filter {
    name   = "architecture"
    values = ["x86_64"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  filter {
    name   = "root-device-type"
    values = ["ebs"]
  }
}

resource "aws_key_pair" "fluent_bit" {
  key_name   = "fluent_bit"
  public_key = file("../aws_key/id_rsa_aws.pub")
}

resource "aws_instance" "aggregator" {
  ami                         = var.environment == "rhel" ? data.aws_ami.rhel8.id : data.aws_ami.rocky8.id
  instance_type               = var.instance_type
  subnet_id                   = aws_subnet.public.id
  private_ip                  = "10.1.4.4"
  associate_public_ip_address = true
  security_groups = [
    aws_security_group.sg.id
  ]
  key_name          = aws_key_pair.fluent_bit.id
  availability_zone = var.availability-zone

  depends_on = [aws_internet_gateway.gw]

  tags = {
    Name = "benchmarking on aggregator"
  }
}

resource "aws_instance" "collector" {
  ami                         = var.environment == "rhel" ? data.aws_ami.rhel8.id : data.aws_ami.rocky8.id
  instance_type               = var.instance_type
  subnet_id                   = aws_subnet.public.id
  private_ip                  = "10.1.4.5"
  associate_public_ip_address = true
  security_groups = [
    aws_security_group.sg.id
  ]
  key_name          = aws_key_pair.fluent_bit.id
  availability_zone = var.availability-zone

  depends_on = [aws_internet_gateway.gw]

  dynamic "ebs_block_device" {
    for_each = var.extra_block_devices
    content {
      delete_on_termination = "true"
      device_name           = ebs_block_device.value.device_name
      volume_type           = ebs_block_device.value.volume_type
      volume_size           = ebs_block_device.value.volume_size
    }
  }

  tags = {
    Name = "benchmarking on collector"
  }

  # make script from template
  provisioner "file" {
    destination = "/tmp/script.sh"
    content = templatefile(
      "${path.module}/script.sh.tpl",
      {
        "connecting_user": var.environment == "rhel" ? "ec2-user" : "rocky"
        "mount_point": (var.instance_type == "i3en.large" || var.instance_type == "i3en.2xlarge" ) ? "/dev/nvme1n1" : "/dev/xvdf"
      }
    )
  }

  provisioner "remote-exec" {
    inline = ["sh /tmp/script.sh"]
  }

  connection {
    type        = "ssh"
    user        = var.environment == "rhel" ? "ec2-user" : "rocky"
    password    = ""
    private_key = file(var.ssh-private-key-path)
    host        = self.public_ip
  }
}
