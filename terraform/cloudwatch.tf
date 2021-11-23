resource "aws_cloudwatch_event_rule" "telegram_daily_reminder" {
  name                = "daily_chron_job"
  schedule_expression = "cron(0 19 ? * MON-FRI *)"  
}

resource "aws_cloudwatch_event_target" "check_foo_every_one_minute" {
  rule      = aws_cloudwatch_event_rule.telegram_daily_reminder.name
  target_id = "lambda"
  arn       = aws_lambda_function.fiemmebot_send_reminder.arn
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_check_foo" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.fiemmebot_send_reminder.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.telegram_daily_reminder.arn
}
