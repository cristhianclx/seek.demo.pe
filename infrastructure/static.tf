locals {
  static_s3_origin_id = "${local.static}-s3"
}

resource "aws_cloudfront_distribution" "static" {
  aliases = [var.static]
  comment = local.static

  default_cache_behavior {
    allowed_methods = ["GET", "HEAD", "OPTIONS"]
    cached_methods  = ["GET", "HEAD", "OPTIONS"]
    compress        = true
    default_ttl     = 0
    forwarded_values {
      query_string = false
      headers = [
        "Access-Control-Request-Headers",
        "Access-Control-Request-Method",
        "Origin",
      ]
      cookies {
        forward = "none"
      }
    }
    min_ttl                = 0
    max_ttl                = 0
    target_origin_id       = local.static_s3_origin_id
    viewer_protocol_policy = "redirect-to-https"
  }

  custom_error_response {
    error_code            = "404"
    error_caching_min_ttl = "0"
    response_code         = "404"
    response_page_path    = "/404.html"
  }

  default_root_object = "index.html"
  enabled             = true
  http_version        = "http2"
  is_ipv6_enabled     = true

  origin {
    domain_name = aws_s3_bucket.static.bucket_regional_domain_name
    origin_id   = local.static_s3_origin_id
    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.static.cloudfront_access_identity_path
    }
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }
  viewer_certificate {
    acm_certificate_arn      = data.aws_acm_certificate.main.arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2018"
  }

  tags = {
    Stage       = var.stage
    Description = local.static
  }

  wait_for_deployment = true
  depends_on = [
    aws_s3_bucket.static,
  ]
}
