resource "aws_ssm_parameter" "api_auth_token" {
  name  = "api_auth_token"
  type  = "SecureString"
  value = var.api_auth_token

  tags = {
    CostCentre = var.billing_code
    Terraform  = true
  }
}
