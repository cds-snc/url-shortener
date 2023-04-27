resource "aws_route53_zone" "url_shortener" {
  name = var.domain

  tags = {
    CostCentre = var.billing_code
    Terraform  = true
  }
}

resource "aws_route53_health_check" "sre_bot_healthcheck" {
  fqdn              = aws_route53_zone.url_shortener.name
  port              = 443
  type              = "HTTPS"
  resource_path     = "/healthcheck"
  failure_threshold = "3"
  request_interval  = "30"

  tags = {
    "CostCentre" = var.billing_code
  }
}
