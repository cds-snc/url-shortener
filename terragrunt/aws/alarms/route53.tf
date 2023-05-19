resource "aws_route53_health_check" "url_shortener" {
  fqdn              = var.domain
  port              = 443
  type              = "HTTPS"
  resource_path     = "/version"
  failure_threshold = "3"
  request_interval  = "30"

  tags = {
    "Name"       = "url-shortener-api"
    "CostCentre" = var.billing_code
  }
}