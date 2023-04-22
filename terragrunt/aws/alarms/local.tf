locals {
  api_cloudwatch_log_group = "/aws/lambda/${var.function_name}"
  error_logged_api         = "ErrorLoggedAPI"
  error_namespace          = "UrlShortener"
  suspicious_logged_api    = "Suspicious"
  warning_logged_api       = "WarningLoggedAPI"
}
