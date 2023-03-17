data "aws_iam_policy_document" "cloudfront_policies" {

  #checkov:skip=CKV_AWS_111: Resource must be "*"
  #checkov:skip=CKV_AWS_109: Resource must be "*"
  # See: https://stackoverflow.com/questions/41991480/the-new-key-policy-will-not-allow-you-to-update-the-key-policy-in-the-future
  # Resource – (Required) In a key policy, you use "*" for the resource, which means "this CMK."
  # A key policy applies only to the CMK it is attached to.
  statement {
    sid    = "AllowKMSAllAccess"
    effect = "Allow"

    principals {
      identifiers = [
        "arn:aws:iam::${var.account_id}:root",
      ]
      type = "AWS"
    }

    actions = [
      "kms:*",
    ]

    resources = [
      "*",
    ]
  }

  statement {
    sid    = "AllowKMSAccessToCloudWatchLogs"
    effect = "Allow"

    principals {
      identifiers = [
        "logs.${var.region}.amazonaws.com",
      ]
      type = "Service"
    }

    actions = [
      "kms:Encrypt*",
      "kms:Decrypt*",
      "kms:ReEncrypt*",
      "kms:GenerateDataKey*",
      "kms:Describe*",
    ]

    resources = [
      "*",
    ]

    condition {
      test     = "ArnEquals"
      variable = "kms:EncryptionContext:aws:logs:arn"
      values = [
        "arn:aws:logs:${var.region}:${var.account_id}:log-group:aws-waf-logs-${var.product_name}",
      ]
    }
  }
}
