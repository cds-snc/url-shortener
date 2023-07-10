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

#
# Route53 DNS logging
#
module "resolver_dns" {
  source            = "github.com/cds-snc/terraform-modules//resolver_dns?ref=v6.1.1"
  vpc_id            = var.vpc_id
  firewall_enabled  = false
  billing_tag_value = var.billing_code
}
