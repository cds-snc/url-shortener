#
# DDoS: CloudFront and Route53
#
resource "aws_cloudwatch_metric_alarm" "cloudfront_ddos" {
  provider = aws.us-east-1

  alarm_name          = "DDoS CloudFront"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "DDoSDetected"
  namespace           = "AWS/DDoSProtection"
  period              = "60"
  statistic           = "Sum"
  threshold           = "0"
  treat_missing_data  = "notBreaching"

  alarm_description = "DDoS detection for CloudFront"
  alarm_actions     = [aws_sns_topic.cloudwatch_warning_us_east.arn]
  ok_actions        = [aws_sns_topic.cloudwatch_warning_us_east.arn]

  dimensions = {
    ResourceArn = var.cloudfront_api_arn
  }
}

resource "aws_cloudwatch_metric_alarm" "route53_ddos" {
  provider = aws.us-east-1

  alarm_name          = "DDoS Route53"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "DDoSDetected"
  namespace           = "AWS/DDoSProtection"
  period              = "60"
  statistic           = "Sum"
  threshold           = "0"
  treat_missing_data  = "notBreaching"

  alarm_description = "DDoS detection for Route53"
  alarm_actions     = [aws_sns_topic.cloudwatch_warning_us_east.arn]
  ok_actions        = [aws_sns_topic.cloudwatch_warning_us_east.arn]

  dimensions = {
    ResourceArn = "arn:aws:route53:::hostedzone/${var.hosted_zone_id}"
  }
}
