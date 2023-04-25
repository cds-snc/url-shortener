module "conformance_pack" {
  source = "github.com/cds-snc/terraform-modules?ref=v5.1.8//cds_conformance_pack"

  cloudwatch_alarm_action_check_param_insufficient_data_action_required = false
  internet_gateway_authorized_vpc_only_param_authorized_vpc_ids         = var.vpc_id

  excluded_rules = [
    "CloudTrailCloudWatchLogsEnabled",      # CloudTrail logs are delivered to S3
    "CloudTrailEncryptionEnabled",          # Default CloudTrail encryption is acceptable
    "LambdaDlqCheck",                       # Lambda API only uses syncronous invocations
    "LambdaFunctionPublicAccessProhibited", # Public access is required for the Lambda API
    "S3BucketLoggingEnabled",               # S3 access logging is monitored through CloudTrail events by CCCS
    "S3BucketReplicationEnabled",           # S3 bucket replication is not required
    "S3BucketVersioningEnabled",            # S3 bucket versioning is not required
    "SnsEncryptedKms",			    # Encryption at rest not required for Alarm topic
  ]

  billing_tag_value = var.billing_code
}
