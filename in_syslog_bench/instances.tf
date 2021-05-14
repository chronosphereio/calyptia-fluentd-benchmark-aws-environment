data "aws_ami" "centos8" {
  most_recent = true

  filter {
    name   = "name"
    values = ["CentOS 8*"]
  }

  filter {
    name   = "architecture"
    values = ["x86_64"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  # CentOS (https://centos.org/download/aws-images/)
  owners = ["125523088429"]
}

data "aws_ami" "rhel8" {
  most_recent = true
  name_regex  = "^RHEL-8.2.0_HVM-"
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

resource "aws_key_pair" "fluentd" {
  key_name   = "fluentd"
  public_key = file("../aws_key/id_rsa_aws.pub")
}

resource "aws_instance" "aggregator" {
  ami                         = var.environment == "rhel" ? data.aws_ami.rhel8.id : data.aws_ami.centos8.id
  instance_type               = "t2.medium"
  subnet_id                   = aws_subnet.public.id
  private_ip                  = "10.2.3.4"
  associate_public_ip_address = true
  security_groups = [
    aws_security_group.sg.id
  ]
  key_name          = aws_key_pair.fluentd.id
  availability_zone = var.availability-zone

  depends_on = [aws_internet_gateway.gw]

  tags = {
    Name = "benchmarking on aggregator"
  }
}

resource "aws_instance" "collector" {
  ami                         = var.environment == "rhel" ? data.aws_ami.rhel8.id : data.aws_ami.centos8.id
  instance_type               = "t2.medium"
  subnet_id                   = aws_subnet.public.id
  private_ip                  = "10.2.3.5"
  associate_public_ip_address = true
  security_groups = [
    aws_security_group.sg.id
  ]
  key_name          = aws_key_pair.fluentd.id
  availability_zone = var.availability-zone

  depends_on = [aws_internet_gateway.gw]

  tags = {
    Name = "benchmarking on collector"
  }
}
