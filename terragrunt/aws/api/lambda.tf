module "url_shortener_lambda" {
  source                 = "github.com/cds-snc/terraform-modules?ref=v5.0.0//lambda"
  name                   = "${var.product_name}-api"
  billing_tag_value      = var.billing_code
  ecr_arn                = aws_ecr_repository.api.arn 
  enable_lambda_insights = true
  image_uri              = "${aws_ecr_repository.api.repository_url}:latest"
  memory                 = 3008
  timeout                = 300
  ephemeral_storage      = 768

  vpc = {
    security_group_ids = [aws_security_group.api.id]
    subnet_ids         = module.url_shortener_vpc.private_subnet_ids
  }

  environment_variables = {
    DOMAIN                    = var.domain
    API_AUTH_TOKEN_SECRET_ARN = aws_ssm_parameter.api_auth_token
  }

  policies = [
    data.aws_iam_policy_document.api_policies.json,
    data.aws_iam_policy_document.api_get_secrets.json,
    sensitive(data.aws_iam_policy_document.api_assume_cross_account.json)
  ]
}

resource "aws_lambda_function_url" "url_shortener_url" {
  function_name      = module.url_shortener_lambda.function_name
  authorization_type = "NONE"
}
