
# Declare a new API Gateway REST API
resource "aws_apigatewayv2_api" "modify_data_api" {
  # The name of the REST API
  name = "modify_data_API"

  # An optional description of the REST API
  description = "The endpoint for any telegram updates"

  protocol_type = "HTTP"

}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.modify_data_api.id
  name        = "default"
  auto_deploy = true

}

resource "aws_apigatewayv2_integration" "telegram_endpoint" {
  api_id = aws_apigatewayv2_api.modify_data_api.id

  integration_uri    = aws_lambda_function.fiemmebot_modify_data.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "telegram_endpoint" {
  api_id = aws_apigatewayv2_api.modify_data_api.id

  route_key = "GET /hello"
  target    = "integrations/${aws_apigatewayv2_integration.telegram_endpoint.id}"
}


resource "aws_lambda_permission" "api_gw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.fiemmebot_modify_data.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.modify_data_api.execution_arn}/*/*/fiemmebot_modify_data_v01"
}

resource "null_resource" "example2" {
  provisioner "local-exec" {
    command     = "curl https://api.telegram.org/bot***REMOVED***/setWebhook?url=${aws_apigatewayv2_stage.default.invoke_url}/modifyData"
    interpreter = ["PowerShell", "-Command"]
  }
}
