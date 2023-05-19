resource "aws_shield_protection" "cloudfront_api" {
  name         = "CloudFrontAPI"
  resource_arn = var.cloudfront_api_arn

  tags = {
    CostCentre = var.billing_code
    Terraform  = true
  }
}

resource "aws_shield_protection" "route53_hosted_zone" {
  name         = "Route53HostedZone"
  resource_arn = "arn:aws:route53:::hostedzone/${var.hosted_zone_id}"

  tags = {
    CostCentre = var.billing_code
    Terraform  = true
  }
}

resource "aws_shield_protection_health_check_association" "cloudfront_api" {
  health_check_arn     = aws_route53_health_check.url_shortener.arn
  shield_protection_id = aws_shield_protection.cloudfront_api.id
}
