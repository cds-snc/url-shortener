#
# SNS: topic & subscription
#
resource "aws_sns_topic" "lambda_dead_letter" {
  name = "cloudwatch-alarms-lambda-dead-letter"
}

resource "aws_sns_topic_subscription" "alert_lambda_dead_letter" {
  topic_arn = aws_sns_topic.lambda_dead_letter.arn
  protocol  = "lambda"
  endpoint  = module.cloudwatch_dead_letter_slack.lambda_arn
}
