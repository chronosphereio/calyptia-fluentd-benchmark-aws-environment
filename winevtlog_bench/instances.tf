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
  public_key = file("../azure_key/id_rsa_azure.pub")
}

resource "aws_instance" "aggregator" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t2.medium"
  subnet_id = "${aws_subnet.public.id}"
  private_ip = "10.0.2.4"
  associate_public_ip_address = true
  security_groups = [
    aws_security_group.aggregator_sg.id
  ]
  key_name      = aws_key_pair.fluentd.id
  availability_zone = "${var.availability-zone}"

  depends_on = [aws_internet_gateway.gw]

  tags = {
    Name = "benchmarking on aggregator"
  }
}

data "aws_ami" "winserv2019" {
  most_recent = true
  filter {
    name   = "name"
    values = ["Windows_Server-2019-English-Full-Base-*"]
  }
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
  owners = ["801119661308"] # Canonical
}

resource "aws_instance" "winserv-2019collector" {
  ami           = data.aws_ami.winserv2019.id
  instance_type = "t2.medium"
  subnet_id = "${aws_subnet.public.id}"
  private_ip = "10.0.2.5"
  associate_public_ip_address = true
  security_groups = [
    aws_security_group.allow_rdp.id
  ]
  key_name      = aws_key_pair.fluentd.id
  availability_zone = "${var.availability-zone}"

  depends_on = [aws_internet_gateway.gw]

  connection {
    type     = "winrm"
    user     = "Administrator"
    password = "${var.windows-adminpassword}"
    # set from default of 5m to 10m to avoid winrm timeout
    timeout  = "10m"
  }

  user_data = <<EOF
<powershell>
  Invoke-WebRequest -Uri https://raw.githubusercontent.com/ansible/ansible/devel/examples/scripts/ConfigureRemotingForAnsible.ps1 -OutFile ConfigureRemotingForAnsible.ps1
  powershell -ExecutionPolicy RemoteSigned .\ConfigureRemotingForAnsible.ps1
  # Set Administrator password for RDP
  $admin = [ADSI]("WinNT://./administrator, user")
  $admin.SetPassword("${var.windows-adminpassword}")
</powershell>
EOF

  tags = {
    CreatedBy = "Terraform"
    Purpose   = "Collect Windows EventLog Benchmark"
    Name = "benchmarking on collector"
  }
}
