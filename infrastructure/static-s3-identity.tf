resource "aws_cloudfront_origin_access_identity" "static" {
  comment = local.static
}

data "aws_iam_policy_document" "static" {
  statement {
    actions = ["s3:GetObject"]
    principals {
      type        = "AWS"
      identifiers = [aws_cloudfront_origin_access_identity.static.iam_arn]
    }
    resources = ["${aws_s3_bucket.static.arn}/*"]
  }
  statement {
    actions = ["s3:ListBucket"]
    principals {
      type        = "AWS"
      identifiers = [aws_cloudfront_origin_access_identity.static.iam_arn]
    }
    resources = [aws_s3_bucket.static.arn]
  }
}

resource "aws_s3_bucket_policy" "static" {
  bucket = aws_s3_bucket.static.id
  policy = data.aws_iam_policy_document.static.json
}
