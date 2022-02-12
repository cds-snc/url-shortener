locals {
  name_prefix     = "${var.product_name}-${var.env}"
  file_queue_name = "${local.name_prefix}-file-queue"
}

module "log_bucket" {
  source            = "github.com/cds-snc/terraform-modules?ref=v0.0.47//S3_log_bucket"
  bucket_name       = "${var.product_name}-${var.env}-logs"
  billing_tag_value = var.billing_code
}

module "file-queue" {
  source      = "github.com/cds-snc/terraform-modules?ref=v0.0.47//S3"
  bucket_name = local.file_queue_name
  lifecycle_rule = [{
    id      = "expire"
    enabled = true
    expiration = {
      days = 7
    }
  }]
  billing_tag_value = var.billing_code
  logging = {
    "target_bucket" = module.log_bucket.s3_bucket_id
    "target_prefix" = local.file_queue_name
  }
}

