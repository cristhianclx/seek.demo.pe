resource "aws_s3_bucket" "static" {
  bucket        = var.static
  force_destroy = true

  tags = {
    Stage = var.stage
  }
}

resource "aws_s3_bucket_ownership_controls" "static" {
  bucket = aws_s3_bucket.static.id
  rule {
    object_ownership = "ObjectWriter"
  }
}

resource "aws_s3_bucket_acl" "static" {
  bucket = aws_s3_bucket.static.id
  acl    = "private"
  depends_on = [
    aws_s3_bucket.static,
    aws_s3_bucket_ownership_controls.static,
  ]
}

resource "aws_s3_bucket_versioning" "static" {
  bucket = aws_s3_bucket.static.id
  versioning_configuration {
    status = "Disabled"
  }
  depends_on = [
    aws_s3_bucket.static,
  ]
}

resource "aws_s3_bucket_public_access_block" "static" {
  bucket                  = aws_s3_bucket.static.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
  depends_on = [
    aws_s3_bucket.static,
  ]
}

resource "aws_s3_bucket_cors_configuration" "static" {
  bucket = aws_s3_bucket.static.id
  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET", "HEAD"]
    allowed_origins = ["https://${var.name}"]
    max_age_seconds = 3000
  }
  depends_on = [
    aws_s3_bucket.static,
  ]
}
