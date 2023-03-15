resource "aws_ssm_parameter" "api_auth_token" {
  name  = "api_auth_token"
  type  = "SecureString"
  value = "API_AUTH_TOKEN=${var.api_auth_token}"

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
