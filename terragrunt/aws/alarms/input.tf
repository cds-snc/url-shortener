variable "cloudfront_api_arn" {
  description = "The ARN of the API's CloudFront distribution."
  type        = string
}

variable "function_name" {
  description = "The name of the API function."
  type        = string
}

variable "hosted_zone_id" {
  description = "The ID of the hosted zone."
  type        = string
}

variable "slack_webhook_url" {
  description = "The URL of the Slack webhook."
  type        = string
  sensitive   = true
}

variable "api_error_threshold" {
  description = "CloudWatch alarm threshold for the URL Shortener API lambda function ERROR logs"
  type        = string
}

variable "api_suspicious_threshold" {
  description = "CloudWatch alarm threshold for the URL Shortener API lambda function SUSPICIOUS logs"
  type        = string
}

variable "api_warning_threshold" {
  description = "CloudWatch alarm threshold for the URL Shortener API lambda function WARNING logs"
  type        = string
}
