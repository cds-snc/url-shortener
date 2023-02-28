#
# SNS: topic & subscription
#
resource "aws_sns_topic" "cloudwatch_warning" {
  name = "cloudwatch-alarms-warning"
}

resource "aws_sns_topic_subscription" "alert_warning" {
  topic_arn = aws_sns_topic.cloudwatch_warning.arn
  protocol  = "lambda"
  endpoint  = module.cloudwatch_alarms_slack.lambda_arn
}