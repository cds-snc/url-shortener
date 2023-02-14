resource "aws_route53_record" "url_shortener_A" {
  zone_id = var.hosted_zone_id
  name    = var.domain
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.url_shortener_api.domain_name
    zone_id                = aws_cloudfront_distribution.url_shortener_api.hosted_zone_id
    evaluate_target_health = false
  }
}

resource "aws_route53_health_check" "url_shortener_A" {
  fqdn              = aws_route53_record.url_shortener_A.fqdn
  port              = 443
  type              = "HTTPS"
  resource_path     = "/healthcheck"
  failure_threshold = "5"
  request_interval  = "30"
  regions           = ["us-east-1", "us-west-1", "us-west-2"]

  tags = {
    CostCentre = var.billing_code
    Terraform  = true
  }
}

#
# Route53 DNS logging and query firewall
#
module "resolver_dns" {
  source           = "github.com/cds-snc/terraform-modules?ref=v5.0.2//resolver_dns"
  vpc_id           = var.vpc_id
  firewall_enabled = true

  allowed_domains = [
    "*.amazonaws.com.",
    "*.gc.ca.",
    "*.canada.ca.",
  ]

  billing_tag_value = var.billing_code
}
