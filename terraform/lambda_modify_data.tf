resource "aws_lambda_function" "fiemmebot_modify_data" {
  filename      = "../modify.zip"
  function_name = "fiemmebot_modify_data_v01"
  role          = "arn:aws:iam::148437798467:role/iam_for_lambda"
  handler       = "modify.lambda_handler"

  runtime = "python3.9"

  environment {
    variables = {
      KEY = "",
      SECRET = "",
      TELEGRAM_TOKEN = "",
    }
  }

  layers = [aws_lambda_layer_version.telegram_bot_libraries.arn]  

}