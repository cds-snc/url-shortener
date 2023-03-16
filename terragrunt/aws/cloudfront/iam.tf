data "aws_iam_policy_document" "cloudfront_policies" {
  statement {
    sid    = "AllowKMSAccessToCloudWatchLogs"
    effect = "Allow"

    principals {
      identifiers = [ "logs.${var.region}.amazonaws.com" ]
      type = "Service"
    }

    actions = [
      "kms:Encrypt*",
      "kms:Decrypt*",
      "kms:ReEncrypt*",
      "kms:GenerateDataKey*",
      "kms:Describe*"
    ]

    resources = [
      "*"
    ]

    condition {
      test     = "ArnEquals"
      variable = "kms:EncryptionContext:aws:logs:arn"
      values = [
        "arn:aws:logs:${var.region}:${var.account_id}:log-group:aws-waf-logs-${var.product_name}/",
      ]
    }
  }
}
