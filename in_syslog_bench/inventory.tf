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
[collector]
${data.aws_eip.collector.public_ip}

[collector:vars]
ansible_port=22
ansible_user=ubuntu
ansible_ssh_private_key_file=${var.ssh-private-key-path}

[aggregator]
${data.aws_eip.aggregator.public_ip}

[aggregator:vars]
ansible_port=22
ansible_user=ubuntu
ansible_ssh_private_key_file=${var.ssh-private-key-path}
EOL
}
