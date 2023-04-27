resource "aws_cloudwatch_log_metric_filter" "url_shortener_api_error" {
  name           = local.error_logged_api
  pattern        = "?ERROR ?Error"
  log_group_name = local.api_cloudwatch_log_group

  metric_transformation {
    name      = local.error_logged_api
    namespace = local.error_namespace
    value     = "1"
  }
}

resource "aws_cloudwatch_metric_alarm" "url_shortener_api_error" {
  alarm_name          = "URL Shortener API Errors"
  alarm_description   = "Errors logged by the URL Shortener API lambda function"
  comparison_operator = "GreaterThanOrEqualToThreshold"

  metric_name        = aws_cloudwatch_log_metric_filter.url_shortener_api_error.metric_transformation[0].name
  namespace          = aws_cloudwatch_log_metric_filter.url_shortener_api_error.metric_transformation[0].namespace
  period             = "60"
  evaluation_periods = "1"
  statistic          = "Sum"
  threshold          = var.api_error_threshold
  treat_missing_data = "notBreaching"

  alarm_actions = [aws_sns_topic.cloudwatch_warning.arn]
  ok_actions    = [aws_sns_topic.cloudwatch_warning.arn]
}

resource "aws_cloudwatch_log_metric_filter" "url_shortener_api_warning" {
  name           = local.warning_logged_api
  pattern        = "?WARNING ?Warning"
  log_group_name = local.api_cloudwatch_log_group

  metric_transformation {
    name      = local.warning_logged_api
    namespace = local.error_namespace
    value     = "1"
  }
}

resource "aws_cloudwatch_metric_alarm" "url_shoretener_api_warning" {
  alarm_name          = "URL Shortener API Warnings"
  alarm_description   = "Warnings logged by the URL Shortener API lambda function"
  comparison_operator = "GreaterThanOrEqualToThreshold"

  metric_name        = aws_cloudwatch_log_metric_filter.url_shortener_api_warning.metric_transformation[0].name
  namespace          = aws_cloudwatch_log_metric_filter.url_shortener_api_warning.metric_transformation[0].namespace
  period             = "60"
  evaluation_periods = "1"
  statistic          = "Sum"
  threshold          = var.api_warning_threshold
  treat_missing_data = "notBreaching"

  alarm_actions = [aws_sns_topic.cloudwatch_warning.arn]
  ok_actions    = [aws_sns_topic.cloudwatch_warning.arn]
}

resource "aws_cloudwatch_log_metric_filter" "url_shortener_api_suspicious" {
  name           = local.suspicious_logged_api
  pattern        = "SUSPICIOUS"
  log_group_name = local.api_cloudwatch_log_group

  metric_transformation {
    name      = local.suspicious_logged_api
    namespace = local.error_namespace
    value     = "1"
  }
}

resource "aws_cloudwatch_metric_alarm" "url_shoretener_api_suspicious" {
  alarm_name          = "URL Shortener API Suspicious"
  alarm_description   = "Suspicious activity by users of the URL Shortener API lambda function over 5 minutes"
  comparison_operator = "GreaterThanOrEqualToThreshold"

  metric_name        = aws_cloudwatch_log_metric_filter.url_shortener_api_suspicious.metric_transformation[0].name
  namespace          = aws_cloudwatch_log_metric_filter.url_shortener_api_suspicious.metric_transformation[0].namespace
  period             = "300"
  evaluation_periods = "1"
  statistic          = "Sum"
  threshold          = var.api_suspicious_threshold
  treat_missing_data = "notBreaching"

  alarm_actions = [aws_sns_topic.cloudwatch_warning.arn]
  ok_actions    = [aws_sns_topic.cloudwatch_warning.arn]
}