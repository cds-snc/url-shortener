resource "aws_ssm_parameter" "api_auth_token" {
  name  = "api_auth_token"
  type  = "SecureString"
  value = "API_AUTH_TOKEN=${var.api_auth_token}"

  tags = {
    CostCentre = var.billing_code
    Terraform  = true
  }
}
