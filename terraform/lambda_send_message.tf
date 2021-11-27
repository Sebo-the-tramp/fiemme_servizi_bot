resource "aws_lambda_function" "fiemmebot_send_reminder" {
  filename      = "../send.zip"
  function_name = "fiemmebot_send_reminder_v01"
  role          = "arn:aws:iam::148437798467:role/iam_for_lambda"
  handler       = "modify.lambda_handler.py"
  runtime       = "python3.9"

  environment {
    variables = {
      KEY            = var.key,
      SECRET         = var.secret,
      TELEGRAM_TOKEN = var.telegram_token,
    }
  }

  layers = [aws_lambda_layer_version.telegram_bot_libraries.arn]

}
