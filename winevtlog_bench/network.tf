# Create a VPC
resource "aws_vpc" "fluentd" {
  cidr_block = "10.0.0.0/16"
  enable_dns_hostnames             = true
  enable_dns_support               = true
}

resource "aws_internet_gateway" "gw" {
  vpc_id = "${aws_vpc.fluentd.id}"

  tags = {
    Name = "Internet Gateway by Terraform"
  }
}

resource "aws_route_table" "r" {
  vpc_id = "${aws_vpc.fluentd.id}"

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = "${aws_internet_gateway.gw.id}"
  }

  tags = {
    Name = "Public route table by Terraform"
  }
}

resource "aws_subnet" "public" {
  vpc_id = "${aws_vpc.fluentd.id}"
  cidr_block = "10.0.2.0/24"
  availability_zone = "${var.availability-zone}"

  tags = {
    Name = "Public Subnet by Terraform"
  }
}

resource "aws_route_table_association" "a" {
  subnet_id = "${aws_subnet.public.id}"
  route_table_id = "${aws_route_table.r.id}"
}

resource "aws_security_group" "aggregator_sg" {
  name        = "aggregator sg"
  description = "Allow ssh/icmp inbound traffic"
  vpc_id      = aws_vpc.fluentd.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = -1
    to_port = -1
    protocol = "icmp"
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

resource "aws_security_group" "allow_rdp" {
  name        = "allow_rdp"
  description = "Allow RDP/icmp inbound traffic"
  vpc_id      = aws_vpc.fluentd.id

  ingress {
    description      = "RDP from VPC"
    from_port        = 3389
    to_port          = 3389
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
  }

  ingress {
    description      = "WinRM from VPC"
    from_port        = 5985
    to_port          = 5986
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
  }

  ingress {
    from_port = -1
    to_port = -1
    protocol = "icmp"
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
  associate_with_private_ip = "10.0.2.4"
  instance                  = aws_instance.aggregator.id

  depends_on = [aws_internet_gateway.gw]
}

resource "aws_eip" "collector" {
  vpc                       = true
  associate_with_private_ip = "10.0.2.5"
  instance                  = aws_instance.winserv-2019collector.id

  depends_on = [aws_internet_gateway.gw]
}
