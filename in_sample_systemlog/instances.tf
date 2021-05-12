resource "azurerm_virtual_machine" "linux-collector" {
  name                             = "${var.prefix}-collector-linux-vm"
  location                         = azurerm_resource_group.fluentd-systemlog.location
  resource_group_name              = azurerm_resource_group.fluentd-systemlog.name
  network_interface_ids            = [azurerm_network_interface.linux-collector.id]
  vm_size                          = "Standard_B2S"
  delete_os_disk_on_termination    = true
  delete_data_disks_on_termination = true

  storage_image_reference {
    publisher = var.environment == "rhel" ? "RedHat" : "OpenLogic"
    offer     = var.environment == "rhel" ? "RHEL"   : "CentOS"
    sku       = var.environment == "rhel" ? "7-LVM"  : "7.5"
    version   = "latest"
  }
  storage_os_disk {
    name              = "collector-disk1"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "Standard_LRS"
  }
  os_profile {
    computer_name  = "${var.prefix}-collector-ubuntu"
    admin_username = var.collector-username
    admin_password = var.collector-password
  }
  os_profile_linux_config {
    disable_password_authentication = true

    ssh_keys {
      path     = "/home/${var.collector-username}/.ssh/authorized_keys"
      key_data = file("../aws_key/id_rsa_aws.pub")
    }
  }
  tags = {
    environment = "benchmarking collector"
  }
}
