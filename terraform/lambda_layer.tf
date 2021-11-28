resource "aws_lambda_layer_version" "telegram_bot_libraries" {
  filename            = "../libraries.zip"
  layer_name          = "telegram_bot_libraries"
  compatible_runtimes = ["python3.9"]
}