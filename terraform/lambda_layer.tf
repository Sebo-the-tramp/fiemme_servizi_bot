resource "aws_lambda_layer_version" "telegram_bot_libraries" {
  filename            = "python.zip"
  layer_name          = "lambda_layer_name"
  compatible_runtimes = ["python3.9"]
}