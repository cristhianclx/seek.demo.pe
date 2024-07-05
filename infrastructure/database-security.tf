resource "mongodbatlas_project_ip_access_list" "database" {
  project_id = mongodbatlas_project.database.id
  cidr_block = var.database_ip_access
}
