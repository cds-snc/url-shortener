module "url_shortener_lambda" {
  source                 = "github.com/cds-snc/terraform-modules?ref=v5.0.2//lambda"
  name                   = "${var.product_name}-api"
  billing_tag_value      = var.billing_code
  ecr_arn                = var.ecr_repository_arn
  enable_lambda_insights = true
  image_uri              = "${var.ecr_repository_url}:${var.ecr_tag}"
  memory                 = 3008
  timeout                = 300


  vpc = {
    security_group_ids = [var.api_security_group_id]
    subnet_ids         = var.private_subnet_ids
  }

  environment_variables = {
    API_AUTH_TOKEN_SECRET_ARN = aws_ssm_parameter.api_auth_token.arn
    SHORTENER_DOMAIN          = "https://${var.domain}/"
  }

  policies = [
    data.aws_iam_policy_document.api_policies.json,
  ]
}

resource "aws_lambda_function_url" "url_shortener_url" {
  function_name      = module.url_shortener_lambda.function_name
  authorization_type = "NONE"
}
