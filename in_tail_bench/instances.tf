data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

resource "aws_key_pair" "fluentd" {
  key_name   = "fluentd"
  public_key = file("../aws_key/id_rsa_aws.pub")
}

resource "aws_instance" "aggregator" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = "t2.medium"
  subnet_id                   = aws_subnet.public.id
  private_ip                  = "10.1.3.4"
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
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = "t2.medium"
  subnet_id                   = aws_subnet.public.id
  private_ip                  = "10.1.3.5"
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
