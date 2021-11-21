provider "aws" {
  profile = "default"
  region     = "eu-west-1"
}

resource "aws_cloudwatch_event_target" "scan_ami_lambda_function" {
  rule = aws_cloudwatch_event_rule.scan_ami.name
  arn  = module.lambda_function.lambda_function_arn
}

resource "aws_lambda_layer_version" "telegram_bot_libraries" {
  filename   = "../python.zip"
  layer_name = "lambda_layer_name"

  compatible_runtimes = ["python3.9"]
}

resource "aws_lambda_function" "test_lambda" {
  filename      = "../modify.zip"
  function_name = "lambda_function_name"
  role          = "arn:aws:iam::148437798467:role/iam_for_lambda"
  handler       = "test.py"

  runtime = "python3.9"

  environment {
    variables = {
      foo = "bar"
    }
  }

  layers = [aws_lambda_layer_version.telegram_bot_libraries.arn]

}
