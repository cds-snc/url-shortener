module "url_shortener_lambda" {
  source                 = "github.com/cds-snc/terraform-modules//lambda?ref=v6.1.1"
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
    ALLOWED_EMAIL_DOMAINS      = "canada.ca,gc.ca,cds-snc.ca"
    ALLOWED_SHORTENED_DOMAINS  = "canada.ca,gc.ca"
    NOTIFY_CONTACT_TEMPLATE    = "47a6be8d-c472-426e-81bb-af1bb89aca87"
    NOTIFY_MAGIC_LINK_TEMPLATE = "092f910a-c3cd-4a91-901d-a2d93fe1e603"
    SHORTENER_DOMAIN           = "https://${var.domain}/"
    SHORTENER_PATH_LENGTH      = var.shortener_path_length
  }

  policies = [
    data.aws_iam_policy_document.api_policies.json,
  ]
}

resource "aws_lambda_alias" "url_shortener_lambda_alias" {
  name             = "latest"
  description      = "The latest version of the lambda function"
  function_name    = module.url_shortener_lambda.function_name
  function_version = "1"

  lifecycle {
    ignore_changes = [
      function_version,
      routing_config
    ]
  }
}

resource "aws_lambda_function_url" "url_shortener_url" {
  function_name      = module.url_shortener_lambda.function_name
  qualifier          = aws_lambda_alias.url_shortener_lambda_alias.name
  authorization_type = "NONE"
}
