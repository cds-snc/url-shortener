locals {
  disabled_controls = [
    # Lambda 
    {
      control = "aws-foundational-security-best-practices/v/1.0.0/Lambda.1"
      reason  = "Lambda needs to be publicly accessible in order for the application to work"
    },
    {
      control = "aws-foundational-security-best-practices/v/1.0.0/Lambda.3"
      reason  = "The lambdas that are not inside VPC are organization/global account pertaining functions"
    },
    # S3 
    {
      control = "aws-foundational-security-best-practices/v/1.0.0/S3.9"
      reason  = "The S3 buckets are used for storing terraform state and therefore logging is not needed"
    },
    # SNS 
    {
      control = "aws-foundational-security-best-practices/v/1.0.0/SNS.1"
      reason  = "Default encryption is acceptable for Alert messages"
    },
  ]
}

resource "aws_securityhub_standards_control" "disabled_controls" {
  for_each = {
    for c in local.disabled_controls : c.control => c
  }

  standards_control_arn = "arn:aws:securityhub:${var.region}:${var.account_id}:control/${each.value.control}"
  control_status        = "DISABLED"
  disabled_reason       = each.value.reason
}
