data "aws_eip" "collector" {
  id = aws_eip.collector.id
}

output "collector_public_ip_address" {
  value = aws_eip.collector.public_ip
}

data "aws_eip" "aggregator" {
  id = aws_eip.aggregator.id
}

output "aggregator_public_ip_address" {
  value = aws_eip.aggregator.public_ip
}

resource "local_file" "inventory" {
  filename        = "ansible/hosts"
  file_permission = "0644"
  content         = <<EOL
[windows]
${data.aws_eip.collector.public_ip}

[windows:vars]
ansible_user=Administrator
ansible_password=${var.windows-adminpassword}
ansible_port=5986
ansible_connection=winrm
ansible_winrm_server_cert_validation=ignore

[aggregator]
${data.aws_eip.aggregator.public_ip}

[aggregator:vars]
ansible_port=22
ansible_user=ubuntu
ansible_ssh_private_key_file=${var.ssh-private-key-path}
EOL
}
