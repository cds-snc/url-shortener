#
# SNS: topic & subscription
#
resource "aws_sns_topic" "cloudwatch_warning" {
  name = "cloudwatch-alarms-warning"

  tags = {
    CostCentre = var.billing_code
    Terraform  = true
  }
}

resource "aws_sns_topic" "cloudwatch_warning_us_east" {
  provider = aws.us-east-1

  name = "cloudwatch-alarms-warning"

  tags = {
    CostCentre = var.billing_code
    Terraform  = true
  }
}

resource "aws_sns_topic_subscription" "alert_warning" {
  topic_arn = aws_sns_topic.cloudwatch_warning.arn
  protocol  = "https"
  endpoint  = var.slack_webhook_url
}

resource "aws_sns_topic_subscription" "alert_warning_us_east" {
  provider = aws.us-east-1

  topic_arn = aws_sns_topic.cloudwatch_warning_us_east.arn
  protocol  = "https"
  endpoint  = var.slack_webhook_url
}
