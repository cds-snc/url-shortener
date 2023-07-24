module "athena_access_logs" {
  source = "github.com/cds-snc/terraform-modules//athena_access_logs?ref=v6.1.5"

  athena_bucket_name         = module.athena_bucket.s3_bucket_id
  waf_access_queries_create  = true
  waf_access_log_bucket_name = var.cbs_satellite_bucket_name

  billing_tag_value = var.billing_code
}

#
# Hold the Athena data
#
module "athena_bucket" {
  source            = "github.com/cds-snc/terraform-modules//S3?ref=v6.1.5"
  bucket_name       = "${var.product_name}-${var.env}-athena-bucket"
  billing_tag_value = var.billing_code

  lifecycle_rule = [
    {
      id      = "expire-objects-after-7-days"
      enabled = true
      expiration = {
        days                         = 7
        expired_object_delete_marker = false
      }
    },
  ]
}