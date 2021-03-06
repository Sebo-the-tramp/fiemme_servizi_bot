resource "aws_lambda_function" "fiemmebot_send_reminder" {
  filename      = "../send.zip"
  function_name = "fiemmebot_send_reminder_v01"
  role          = "arn:aws:iam::148437798467:role/iam_for_lambda"
  handler       = "send_message.lambda_handler"
  runtime       = "python3.9"

  environment {
    variables = {
      DYNAMO_ACCESS_KEY_ID     = var.key,
      DYNAMO_SECRET_ACCESS_KEY = var.secret,
      TELEGRAM_TOKEN           = var.telegram_token,
    }
  }

  layers = [aws_lambda_layer_version.telegram_bot_libraries.arn]

}
