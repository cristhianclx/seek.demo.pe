output "name" {
  value = var.name
}
output "alb" {
  value = aws_alb.alb.dns_name
}
output "static" {
  value = var.static
}
output "static_s3" {
  value = aws_s3_bucket.static.bucket_regional_domain_name
}
output "static_cf" {
  value = aws_cloudfront_distribution.static.domain_name
}
