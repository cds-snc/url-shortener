locals {
  api_log_group_arn            = "arn:aws:logs:${var.region}:${var.account_id}:log-group:/aws/lambda/${module.url_shortener_lambda.function_name}"
  sentinel_forwarder_layer_arn = "arn:aws:lambda:ca-central-1:283582579564:layer:aws-sentinel-connector-layer:54"
}

module "sentinel_forwarder" {
  source            = "github.com/cds-snc/terraform-modules?ref=v5.1.5//sentinel_forwarder"
  function_name     = "sentinel-cloudwatch-forwarder"
  billing_tag_value = var.billing_code

  layer_arn = local.sentinel_forwarder_layer_arn

  customer_id = var.sentinel_customer_id
  shared_key  = var.sentinel_shared_key

  cloudwatch_log_arns = [local.api_log_group_arn]
}