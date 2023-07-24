locals {
  api_log_group_name           = "/aws/lambda/${module.url_shortener_lambda.function_name}"
  api_log_group_arn            = "arn:aws:logs:${var.region}:${var.account_id}:log-group:${local.api_log_group_name}"
  sentinel_forwarder_layer_arn = "arn:aws:lambda:ca-central-1:283582579564:layer:aws-sentinel-connector-layer:58"
}

module "sentinel_forwarder" {
  source            = "github.com/cds-snc/terraform-modules//sentinel_forwarder?ref=v6.1.5"
  function_name     = "sentinel-cloudwatch-forwarder"
  billing_tag_value = var.billing_code

  layer_arn = local.sentinel_forwarder_layer_arn

  customer_id = var.sentinel_customer_id
  shared_key  = var.sentinel_shared_key

  cloudwatch_log_arns = [local.api_log_group_arn]
}

resource "aws_cloudwatch_log_subscription_filter" "api_request" {
  name            = "API request"
  log_group_name  = local.api_log_group_name
  filter_pattern  = "?INFO ?WARNING ?ERROR"
  destination_arn = module.sentinel_forwarder.lambda_arn
  distribution    = "Random"
}