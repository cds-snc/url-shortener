module "cloudwatch_dead_letter_slack" {
  source = "github.com/cds-snc/terraform-modules?ref=v5.1.5//notify_slack"

  function_name     = "${var.product_name}-cloudwatch-alarms-slack"
  project_name      = var.product_name
  slack_webhook_url = var.slack_webhook_url
  sns_topic_arns = [
    aws_sns_topic.lambda_dead_letter.arn,
  ]

  billing_tag_value = var.billing_code
}
