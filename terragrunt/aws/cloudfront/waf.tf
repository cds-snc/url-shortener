resource "aws_wafv2_web_acl" "api_waf" {
  provider = aws.us-east-1

  name        = "${var.product_name}-waf"
  description = "WAF for URL shortener API"
  scope       = "CLOUDFRONT"

  tags = {
    CostCentre = var.billing_code
    Terraform  = true
  }

  default_action {
    allow {}
  }

  rule {
    name     = "AWSRoute53HealthchecksAllRegions"
    priority = 3

    action {
      dynamic "allow" {
        for_each = var.enable_waf == true ? [""] : []
        content {
        }
      }

      dynamic "count" {
        for_each = var.enable_waf == false ? [""] : []
        content {
        }
      }
    }

    statement {
      ip_set_reference_statement {
        arn = aws_wafv2_ip_set.aws-route53-healthchecks-all-regions.arn
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "AWSRoute53HealthchecksAllRegions"
      sampled_requests_enabled   = true
    }
  }

  rule {
    name     = "APIInvalidPath"
    priority = 5

    action {
      dynamic "block" {
        for_each = var.enable_waf == true ? [""] : []
        content {
        }
      }

      dynamic "count" {
        for_each = var.enable_waf == false ? [""] : []
        content {
        }
      }
    }

    statement {
      not_statement {
        statement {
          regex_pattern_set_reference_statement {
            arn = aws_wafv2_regex_pattern_set.valid_uri_paths.arn
            field_to_match {
              uri_path {}
            }
            text_transformation {
              priority = 1
              type     = "COMPRESS_WHITE_SPACE"
            }
            text_transformation {
              priority = 2
              type     = "LOWERCASE"
            }
          }
        }
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "APIInvalidPaths"
      sampled_requests_enabled   = true
    }
  }

  rule {
    name     = "AWSManagedRulesAmazonIpReputationList"
    priority = 10

    override_action {
      dynamic "none" {
        for_each = var.enable_waf == true ? [""] : []
        content {
        }
      }

      dynamic "count" {
        for_each = var.enable_waf == false ? [""] : []
        content {
        }
      }
    }

    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesAmazonIpReputationList"
        vendor_name = "AWS"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "AWSManagedRulesAmazonIpReputationList"
      sampled_requests_enabled   = true
    }
  }

  rule {
    name     = "APIRateLimit"
    priority = 20

    action {
      dynamic "block" {
        for_each = var.enable_waf == true ? [""] : []
        content {
        }
      }

      dynamic "count" {
        for_each = var.enable_waf == false ? [""] : []
        content {
        }
      }
    }

    statement {
      rate_based_statement {
        limit              = 2000
        aggregate_key_type = "IP"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "APIRateLimit"
      sampled_requests_enabled   = true
    }
  }

  rule {
    name     = "AWSManagedRulesCommonRuleSet"
    priority = 30

    override_action {
      dynamic "none" {
        for_each = var.enable_waf == true ? [""] : []
        content {
        }
      }

      dynamic "count" {
        for_each = var.enable_waf == false ? [""] : []
        content {
        }
      }
    }

    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesCommonRuleSet"
        vendor_name = "AWS"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "AWSManagedRulesCommonRuleSet"
      sampled_requests_enabled   = true
    }
  }

  rule {
    name     = "AWSManagedRulesKnownBadInputsRuleSet"
    priority = 40

    override_action {
      dynamic "none" {
        for_each = var.enable_waf == true ? [""] : []
        content {
        }
      }

      dynamic "count" {
        for_each = var.enable_waf == false ? [""] : []
        content {
        }
      }
    }

    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesKnownBadInputsRuleSet"
        vendor_name = "AWS"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "AWSManagedRulesKnownBadInputsRuleSet"
      sampled_requests_enabled   = true
    }
  }

  rule {
    name     = "AWSManagedRulesLinuxRuleSet"
    priority = 50

    override_action {
      dynamic "none" {
        for_each = var.enable_waf == true ? [""] : []
        content {
        }
      }

      dynamic "count" {
        for_each = var.enable_waf == false ? [""] : []
        content {
        }
      }
    }

    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesLinuxRuleSet"
        vendor_name = "AWS"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "AWSManagedRulesLinuxRuleSet"
      sampled_requests_enabled   = true
    }
  }

  visibility_config {
    cloudwatch_metrics_enabled = true
    metric_name                = "api"
    sampled_requests_enabled   = false
  }
}

resource "aws_wafv2_regex_pattern_set" "valid_uri_paths" {
  provider    = aws.us-east-1
  name        = "valid-api-paths"
  description = "Regex to match the valid paths of hte API"
  scope       = "CLOUDFRONT"

  # ops
  regular_expression {
    regex_string = "^/(version|healthcheck|openapi.json|.well-known/security.txt)$"
  }

  # api call to shorten url
  regular_expression {
    regex_string = "^/v1$"
  }

  # allow base64 and get short url
  regular_expression {
    regex_string = "^/[0-9A-Za-z]{8}$"
  }

  # allow homepage 
  regular_expression {
    regex_string = "^/$"
  }

  # allow static files 
  regular_expression {
    regex_string = "^/static/*"
  }

  tags = {
    CostCentre = var.billing_code
    Terraform  = true
  }
}

resource "aws_wafv2_ip_set" "aws-route53-healthchecks-all-regions" {
  provider           = aws.us-east-1
  name               = "aws-route53-healthchecks-all-regions"
  description        = "AWS Route 53 Healthchecks all regions"
  scope              = "CLOUDFRONT"
  ip_address_version = "IPV4"
  addresses          = [
    "15.177.0.0/18",
    "52.80.197.0/25",
    "52.80.197.128/25",
    "52.80.198.0/25",
    "52.83.34.128/25",
    "52.83.35.0/25",
    "52.83.35.128/25",
    "54.248.220.0/26",
    "54.250.253.192/26",
    "54.251.31.128/26",
    "54.255.254.192/26",
    "54.252.254.192/26",
    "54.252.79.128/26",
    "176.34.159.192/26",
    "54.228.16.0/26",
    "177.71.207.128/26",
    "54.232.40.64/26",
    "107.23.255.0/26",
    "54.243.31.192/26",
    "54.183.255.128/26",
    "54.241.32.64/26",
    "54.244.52.192/26",
    "54.245.168.0/26",
  ]

  tags = {
    CostCentre = var.billing_code
    Terraform  = true
  }
}

resource "aws_kms_key" "wafv2-log-group-kms-key" {
  provider                 = aws.us-east-1
  description              = "WAF Cloudwatch logs KMS key"
  key_usage                = "ENCRYPT_DECRYPT"
  customer_master_key_spec = "SYMMETRIC_DEFAULT"
  is_enabled               = true
  enable_key_rotation      = true
  policy                   = data.aws_iam_policy_document.cloudfront_policies.json

  tags = {
    CostCentre = var.billing_code
    Terraform  = true
  }
}

resource "aws_cloudwatch_log_group" "wafv2-log-group" {
  provider          = aws.us-east-1
  name              = "aws-waf-logs-${var.product_name}"
  retention_in_days = 90
  kms_key_id        = aws_kms_key.wafv2-log-group-kms-key.arn

  tags = {
    CostCentre = var.billing_code
    Terraform  = true
  }
}

resource "aws_wafv2_web_acl_logging_configuration" "waf_logging_configuration" {
  provider                = aws.us-east-1
  log_destination_configs = [aws_cloudwatch_log_group.wafv2-log-group.arn]
  resource_arn            = aws_wafv2_web_acl.api_waf.arn
  depends_on              = [aws_cloudwatch_log_group.wafv2-log-group]
}

resource "aws_cloudwatch_log_metric_filter" "wafv2-log-metric-filter" {
  provider       = aws.us-east-1
  name           = "aws-waf-logs-${var.product_name}-metric-filter"
  pattern        = "{ $.httpRequest.uri != \"/version\" }"
  log_group_name = aws_cloudwatch_log_group.wafv2-log-group.name

  metric_transformation {
    name      = "RequestCount"
    namespace = "UserTraffic"
    value     = "1"
  }
}

resource "aws_cloudwatch_log_metric_filter" "wafv2-log-metric-filter-health-check" {
  provider       = aws.us-east-1
  name           = "aws-waf-logs-${var.product_name}-metric-filter-health-check"
  pattern        = "{ $.httpRequest.uri = \"/version\" }"
  log_group_name = aws_cloudwatch_log_group.wafv2-log-group.name

  metric_transformation {
    name      = "RequestCount"
    namespace = "HealthCheckTraffic"
    value     = "1"
  }
}
