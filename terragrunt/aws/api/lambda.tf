module "api" {
  source                   = "github.com/cds-snc/terraform-modules?ref=v0.0.45//lambda"
  name                     = "api"
  billing_tag_value        = var.billing_code
  allow_api_gateway_invoke = true
  api_gateway_source_arn   = "${aws_api_gateway_rest_api.api.execution_arn}/*/*"
  ecr_arn                  = aws_ecr_repository.api.arn
  enable_lambda_insights   = true
  image_uri                = "${aws_ecr_repository.api.repository_url}:latest"
  timeout                  = 120

  vpc = {
    security_group_ids = [module.rds.proxy_security_group_id, aws_security_group.api.id]
    subnet_ids         = module.vpc.private_subnet_ids
  }

  environment_variables = {
    API_AUTH_TOKEN               = var.api_auth_token
    SQLALCHEMY_DATABASE_URI      = module.rds.proxy_connection_string_value
    OPENAPI_URL                  = "/openapi.json" # Enable /docs api endpoint
  }

  policies = [
    data.aws_iam_policy_document.api_policies.json,
  ]
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_lambda" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = module.api.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.assemblyline_rescan_every_24_hours.arn
}
