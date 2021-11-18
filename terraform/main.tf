resource "null_resource" "install_libraries" {
  provisioner "local-exec" {
    command = "python -m pip install python-telegram-bot -t ../libraries/python"
    interpreter = ["PowerShell", "-Command"]
  }
}

