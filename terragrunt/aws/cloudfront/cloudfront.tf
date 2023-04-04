resource "aws_cloudfront_distribution" "url_shortener_api" {
  enabled     = true
  aliases     = [var.domain]
  price_class = "PriceClass_100"
  web_acl_id  = aws_wafv2_web_acl.api_waf.arn

  origin {
    domain_name = split("/", var.function_url)[2]
    origin_id   = var.function_name

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_read_timeout    = 60
      origin_protocol_policy = "https-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  default_cache_behavior {
    allowed_methods = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods  = ["GET", "HEAD"]

    target_origin_id           = var.function_name
    viewer_protocol_policy     = "redirect-to-https"
    response_headers_policy_id = aws_cloudfront_response_headers_policy.security_headers_api.id

    compress = true

    cache_policy_id          = "4135ea2d-6df8-44a3-9df3-4b5a84be39ad" # CachingDisabled https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/using-managed-cache-policies.html
    origin_request_policy_id = "b689b0a8-53d0-40ab-baf2-68738e2966ac" # AllViewerExceptHostHeader https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/using-managed-origin-request-policies.html
  }

  # Prevent caching of healthcheck calls
  ordered_cache_behavior {
    path_pattern    = "/healthcheck"
    allowed_methods = ["GET", "HEAD"]
    cached_methods  = ["GET", "HEAD"]

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    target_origin_id           = var.function_name
    viewer_protocol_policy     = "redirect-to-https"
    response_headers_policy_id = aws_cloudfront_response_headers_policy.security_headers_api.id

    min_ttl     = 0
    default_ttl = 0
    max_ttl     = 0
    compress    = true
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn      = aws_acm_certificate_validation.url_shortener_certificate_validation.certificate_arn
    minimum_protocol_version = "TLSv1.2_2021"
    ssl_support_method       = "sni-only"
  }

  tags = {
    CostCentre = var.billing_code
    Terraform  = true
  }
}

resource "aws_cloudfront_response_headers_policy" "security_headers_api" {
  name = "url-shortener-security-headers-api"

  security_headers_config {
    frame_options {
      frame_option = "DENY"
      override     = true
    }
    content_type_options {
      override = true
    }
    content_security_policy {
      content_security_policy = "report-uri https://csp-report-to.security.cdssandbox.xyz/report; default-src 'none'; script-src 'self' 'unsafe-inline' https://unpkg.com/@cdssnc/ https://${var.domain}/static/js/ https://kit.fontawesome.com; font-src 'self' https://kit.fontawesome.com https://fonts.googleapis.com https://fonts.gstatic.com; connect-src 'self'; img-src 'self' https://${var.domain}/static/img/ http://www.w3.org/2000; style-src 'self' 'unsafe-inline' https://${var.domain}/static/css/ https://unpkg.com/@cdssnc/ https://kit.fontawesome.com https://fonts.googleapis.com; frame-ancestors 'self'; form-action 'self';"
      override                = false
    }
    referrer_policy {
      override        = true
      referrer_policy = "same-origin"
    }
    strict_transport_security {
      override                   = true
      access_control_max_age_sec = 31536000
      include_subdomains         = true
      preload                    = true
    }
    xss_protection {
      override   = true
      mode_block = true
      protection = true
    }
  }
}
