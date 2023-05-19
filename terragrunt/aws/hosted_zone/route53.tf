resource "aws_route53_zone" "url_shortener" {
  name = var.domain

  tags = {
    CostCentre = var.billing_code
    Terraform  = true
  }
}
