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

resource "aws_ssm_parameter" "hashing_peppers" {
  name  = "hashing_peppers"
  type  = "SecureString"
  value = "PEPPERS=${var.hashing_peppers}"

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
