data "aws_iam_policy_document" "api_policies" {

  statement {

    effect = "Allow"

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]

    resources = [
      "arn:aws:logs:${var.region}:${var.account_id}:log-group:*"
    ]
  }

  statement {

    effect = "Allow"

    actions = [
      "states:ListStateMachines",
      "states:ListActivities",
      "states:CreateActivity",
      "states:DescribeExecution",
      "states:StartExecution",
    ]

    resources = [
      "arn:aws:states:${var.region}:${var.account_id}:*"
    ]
  }

  statement {

    effect = "Allow"

    actions = [
      "events:PutTargets",
      "events:PutRule",
      "events:DescribeRule"
    ]

    resources = [
      "arn:aws:events:${var.region}:${var.account_id}:*"
    ]
  }

  statement {

    effect = "Allow"

    actions = [
      "dynamodb:GetItem",
      "dynamodb:DeleteItem",
      "dynamodb:PutItem",
    ]

    resources = [
      "arn:aws:dynamodb:${var.region}:${var.account_id}:table/${var.url_shortener_table_name}"
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "ssm:GetParameters",
    ]
    resources = [
      aws_ssm_parameter.api_auth_token.arn
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "lambda:InvokeFunction"
    ]
    resources = [
      module.url_shortener_lambda.function_arn
    ]
  }
}
