resource "aws_lambda_function" "fiemmebot_send_reminder" {
  filename      = "../modify.zip"
  function_name = "fiemmebot_send_reminder_v01"
  role          = "arn:aws:iam::148437798467:role/iam_for_lambda"
  handler       = "send_message.py"

  runtime = "python3.9"

  environment {
    variables = {
      foo = "bar"
    }
  }

  layers = [aws_lambda_layer_version.telegram_bot_libraries.arn]  

}