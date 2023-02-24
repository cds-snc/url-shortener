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
    name     = "APIInvalidPath"
    priority = 1

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
    regex_string = "^/[0-9A-Za-z+_/=]{8}$"
  }

  # allow homepage 
  regular_expression {
    regex_string = "^/$"
  }

  tags = {
    CostCentre = var.billing_code
    Terraform  = true
  }
}
