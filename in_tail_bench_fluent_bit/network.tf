# Create a VPC
resource "aws_vpc" "fluent_bit" {
  cidr_block           = "10.1.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
}

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.fluent_bit.id

  tags = {
    Name = "Internet Gateway by Terraform"
  }
}

resource "aws_route_table" "r" {
  vpc_id = aws_vpc.fluent_bit.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }

  tags = {
    Name = "Public route table by Terraform"
  }
}

resource "aws_subnet" "public" {
  vpc_id            = aws_vpc.fluent_bit.id
  cidr_block        = "10.1.4.0/24"
  availability_zone = var.availability-zone

  tags = {
    Name = "Public Subnet by Terraform"
  }
}

resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.r.id
}

resource "aws_security_group" "sg" {
  name        = "Linux sg"
  description = "Allow ssh/icmp/https payload inbound traffic"
  vpc_id      = aws_vpc.fluent_bit.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8443
    to_port     = 8443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 9090
    to_port     = 9090
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = -1
    to_port     = -1
    protocol    = "icmp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    environment = "Created with Terraform"
  }
}

resource "aws_eip" "aggregator" {
  vpc                       = true
  associate_with_private_ip = "10.1.4.4"
  instance                  = aws_instance.aggregator.id

  depends_on = [aws_internet_gateway.gw]
}

resource "aws_eip" "collector" {
  vpc                       = true
  associate_with_private_ip = "10.1.4.5"
  instance                  = aws_instance.collector.id

  depends_on = [aws_internet_gateway.gw]
}
