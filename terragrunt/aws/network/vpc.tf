#
# VPC
#

module "url_shortener_vpc" {
  source            = "github.com/cds-snc/terraform-modules//vpc?ref=v6.1.5"
  name              = var.product_name
  billing_tag_value = var.billing_code
  high_availability = true
  enable_flow_log   = false # These are created separately for CBS
  block_ssh         = true
  block_rdp         = true

  single_nat_gateway = var.env != "production"

  allow_https_request_out          = true
  allow_https_request_out_response = true
  allow_https_request_in           = true
  allow_https_request_in_response  = true
}

#
# VPC endpoints
#
resource "aws_vpc_endpoint" "logs" {
  vpc_id              = module.url_shortener_vpc.vpc_id
  vpc_endpoint_type   = "Interface"
  service_name        = "com.amazonaws.${var.region}.logs"
  private_dns_enabled = true
  security_group_ids = [
    aws_security_group.vpc_endpoint.id,
  ]
  subnet_ids = module.url_shortener_vpc.private_subnet_ids
}

resource "aws_vpc_endpoint" "dynamodb" {
  vpc_id            = module.url_shortener_vpc.vpc_id
  vpc_endpoint_type = "Gateway"
  service_name      = "com.amazonaws.${var.region}.dynamodb"
  route_table_ids   = [module.url_shortener_vpc.main_route_table_id]
}

resource "aws_vpc_endpoint" "s3" {
  vpc_id            = module.url_shortener_vpc.vpc_id
  vpc_endpoint_type = "Gateway"
  service_name      = "com.amazonaws.${var.region}.s3"
  route_table_ids   = [module.url_shortener_vpc.main_route_table_id]
}
