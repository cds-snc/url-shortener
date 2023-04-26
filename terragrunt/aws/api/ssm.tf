resource "aws_ssm_parameter" "auth_token_app" {
  name  = "auth_token_app"
  type  = "SecureString"
  value = "AUTH_TOKEN_APP=${var.auth_token_app}"

  tags = {
    CostCentre = var.billing_code
    Terraform  = true
  }
}

resource "aws_ssm_parameter" "auth_token_notify" {
  name  = "auth_token_notify"
  type  = "SecureString"
  value = "AUTH_TOKEN_NOTIFY=${var.auth_token_notify}"

  tags = {
    CostCentre = var.billing_code
    Terraform  = true
  }
}

resource "aws_ssm_parameter" "cloudfront_header" {
  name  = "cloudfront_header"
  type  = "SecureString"
  value = "CLOUDFRONT_HEADER=${var.cloudfront_header}"

  tags = {
    CostCentre = var.billing_code
    Terraform  = true
  }
}

resource "aws_ssm_parameter" "hashing_peppers" {
  name  = "hashing_peppers"
  type  = "SecureString"
  value = "PEPPERS=${var.hashing_peppers}"

  tags = {
    CostCentre = var.billing_code
    Terraform  = true
  }
}

resource "aws_ssm_parameter" "login_token_salt" {
  name  = "login_token_salt"
  type  = "SecureString"
  value = "LOGIN_TOKEN_SALT=${var.login_token_salt}"

  tags = {
    CostCentre = var.billing_code
    Terraform  = true
  }
}

resource "aws_ssm_parameter" "notify_api_key" {
  name  = "notify_api_key"
  type  = "SecureString"
  value = "NOTIFY_API_KEY=${var.notify_api_key}"

  tags = {
    CostCentre = var.billing_code
    Terraform  = true
  }
}

resource "aws_ssm_parameter" "notify_contact_email" {
  name  = "notify_contact_email"
  type  = "SecureString"
  value = "NOTIFY_CONTACT_EMAIL=${var.notify_contact_email}"

  tags = {
    CostCentre = var.billing_code
    Terraform  = true
  }
}
