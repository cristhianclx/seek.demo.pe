resource "aws_s3_object" "static_files" {
  for_each = fileset(var.files_static, "**")

  acl            = "private"
  bucket         = aws_s3_bucket.static.id
  content_base64 = filebase64("${var.files_static}/${each.value}")
  content_type   = lookup(var.files_types, local.static_files_suffixes[each.value], var.files_types_default)
  etag           = filemd5("${var.files_static}/${each.value}")
  key            = each.value
}
