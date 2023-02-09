# 
# Security Groups for the VPC URL shortener
#

resource "aws_security_group" "api" {

  name        = "${var.product_name}_api_sg"
  description = "SG for the URL shortener API"

  vpc_id = module.url_shortener_vpc.vpc_id

  tags = {
    CostCentre = var.billing_code
    Name       = "${var.product_name}_api_sg"
  }
}

resource "aws_security_group" "vpc_endpoint" {
  name        = "vpc_endpoints"
  description = "PrivateLink VPC endpoints"
  vpc_id      = module.url_shortener_vpc.vpc_id

  tags = {
    Name       = "${var.product_name}_api_sg"
    CostCentre = var.billing_code
    Terraform  = true
  }
}

resource "aws_security_group_rule" "vpc_endpoint_interface_ingress" {
  description              = "Ingress from the API security group to the private interface endpoints"
  type                     = "ingress"
  from_port                = 443
  to_port                  = 443
  protocol                 = "tcp"
  security_group_id        = aws_security_group.vpc_endpoint.id
  source_security_group_id = aws_security_group.api.id
}

resource "aws_security_group_rule" "vpc_endpoint_dynamodb_ingress" {
  description       = "Ingress from the private DynamoDB endpoint"
  type              = "ingress"
  from_port         = 443
  to_port           = 443
  protocol          = "tcp"
  security_group_id = aws_security_group.vpc_endpoint.id
  prefix_list_ids = [
    aws_vpc_endpoint.dynamodb.prefix_list_id
  ]
}

resource "aws_security_group_rule" "s3_private_endpoint_ingress" {
  description       = "Ingress from the private S3 endpoint"
  type              = "ingress"
  from_port         = 443
  to_port           = 443
  protocol          = "tcp"
  security_group_id = aws_security_group.vpc_endpoint.id
  prefix_list_ids = [
    aws_vpc_endpoint.s3.prefix_list_id
  ]
}

resource "aws_flow_log" "cloud_based_sensor" {
  log_destination      = "arn:aws:s3:::${var.cbs_satellite_bucket_name}/vpc_flow_logs/"
  log_destination_type = "s3"
  traffic_type         = "ALL"
  vpc_id               = module.url_shortener_vpc.vpc_id
  log_format           = "$${vpc-id} $${version} $${account-id} $${interface-id} $${srcaddr} $${dstaddr} $${srcport} $${dstport} $${protocol} $${packets} $${bytes} $${start} $${end} $${action} $${log-status} $${subnet-id} $${instance-id}"

  tags = {
    CostCentre = var.billing_code
    Terraform  = true
  }
}
