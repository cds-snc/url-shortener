module "conformance_pack" {
  source                                                        = "github.com/cds-snc/terraform-modules?ref=v5.1.8//cds_conformance_pack"
  internet_gateway_authorized_vpc_only_param_authorized_vpc_ids = var.vpc_id
  excluded_rules                                                = ["LambdaDlqCheck", "LambdaFunctionPublicAccessProhibited", "S3BucketLoggingEnabled"]
  billing_tag_value                                             = var.billing_code
}
