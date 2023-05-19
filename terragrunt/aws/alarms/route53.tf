resource "aws_route53_health_check" "url_shortener" {
  name              = "UrlShortenerAPI"
  fqdn              = var.domain
  port              = 443
  type              = "HTTPS"
  resource_path     = "/version"
  failure_threshold = "3"
  request_interval  = "30"

  tags = {
    "CostCentre" = var.billing_code
  }
}