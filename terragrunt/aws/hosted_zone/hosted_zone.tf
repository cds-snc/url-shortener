resource "aws_route53_zone" "url_shortener" {
  name = var.hosted_zone_name

  tags = {
    CostCenter = var.billing_code
  }
}
