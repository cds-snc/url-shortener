data "aws_iam_policy_document" "api_policies" {

  statement {

    effect = "Allow"

    actions = [
      "dynamodb:GetItem",
      "dynamodb:DeleteItem",
      "dynamodb:PutItem",
      "dynamodb:DescribeTable",
      "dynamodb:Query",
    ]

    resources = [
      "arn:aws:dynamodb:${var.region}:${var.account_id}:table/${var.url_shortener_table_name}",
      "arn:aws:dynamodb:${var.region}:${var.account_id}:table/${var.url_shortener_table_name}/index/emailIndex",
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "ssm:GetParameters",
    ]
    resources = [
      aws_ssm_parameter.auth_token_app.arn,
      aws_ssm_parameter.auth_token_notify.arn,
      aws_ssm_parameter.hashing_peppers.arn,
      aws_ssm_parameter.notify_api_key.arn
    ]
  }
}
