resource "aws_ssm_parameter" "database_connection" {
  name        = "/${var.main}/${var.stage}/database/connection"
  description = "${local.main}-${var.stage}--database-connection"
  type        = "String"
  value       = mongodbatlas_cluster.database.connection_strings.0.standard_srv

  tier = "Standard"
}
resource "aws_ssm_parameter" "database_user" {
  name        = "/${var.main}/${var.stage}/database/user"
  description = "${local.main}-${var.stage}--database-user"
  type        = "String"
  value       = mongodbatlas_database_user.database_credentials_user.username

  tier = "Standard"
}
resource "aws_ssm_parameter" "database_password" {
  name        = "/${var.main}/${var.stage}/database/password"
  description = "${local.main}-${var.stage}--database-password"
  type        = "SecureString"
  value       = mongodbatlas_database_user.database_credentials_user.password

  key_id = "alias/aws/ssm"
  tier   = "Standard"
}
