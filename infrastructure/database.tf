resource "mongodbatlas_project" "database" {
  org_id = var.database_organization_id
  name   = "${var.database_project_name}-${var.stage}"
}

resource "mongodbatlas_database_user" "database_credentials_user" {
  username           = "api"
  password           = random_password.database_credentials_password.result
  project_id         = mongodbatlas_project.database.id
  auth_database_name = "admin"
  roles {
    role_name     = "readWrite"
    database_name = "bbdd"
  }
}
resource "random_password" "database_credentials_password" {
  length           = 16
  special          = true
  override_special = "_%@"
}

resource "mongodbatlas_cluster" "database" {
  project_id = mongodbatlas_project.database.id
  name       = "${var.database_project_name}-${var.stage}-cluster"

  provider_name               = var.database_provider
  provider_region_name        = var.database_region
  provider_instance_size_name = var.database_type

  mongo_db_major_version = var.database_version
}
