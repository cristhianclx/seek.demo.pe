variable "stage" {
  description = "stage"
  type        = string
}

variable "main" {
  description = "main"
  type        = string
}

variable "name" {
  description = "name"
  type        = string
}

variable "static" {
  description = "static"
  type        = string
}
variable "files_static" {
  default     = "./files-static"
  description = "files"
  type        = string
}

variable "image_name" {
  description = "image_name"
  type        = string
}
variable "image_owner" {
  description = "image_owner"
  type        = string
}

variable "instance_type" {
  description = "instance_type"
  type        = string
}
variable "instance_disk_type" {
  default     = "gp2"
  description = "instance_disk_type"
  type        = string
}
variable "instance_disk_size" {
  default     = 20
  description = "instance_disk_size"
  type        = number
}

variable "instance_user" {
  description = "instance_user"
  type        = string
}
variable "instance_key_name" {
  description = "instance_key_name"
  type        = string
}
variable "instance_health_check" {
  description = "instance_health_check"
  type        = string
}

variable "instances_scale_desired" {
  default     = 1
  description = "instances_scale_desired"
  type        = number
}
variable "instances_scale_min" {
  default     = 1
  description = "instances_scale_min"
  type        = number
}
variable "instances_scale_max" {
  default     = 1
  description = "instances_scale_max"
  type        = number
}
variable "instance_metrics_cpu_utilization_high_threshold" {
  description = "instance_metrics_cpu_utilization_high_threshold"
  type        = number
}
variable "instance_metrics_cpu_utilization_low_threshold" {
  description = "instance_metrics_cpu_utilization_low_threshold"
  type        = number
}
variable "instances_metrics_healthy_hosts_threshold" {
  description = "instances_metrics_healthy_hosts_threshold"
  type        = number
}
variable "instances_metrics_http_server_errors_threshold" {
  description = "instances_metrics_http_server_errors_threshold"
  type        = number
}
variable "instances_metrics_http_response_time_threshold" {
  description = "instances_metrics_http_response_time_threshold"
  type        = number
}

variable "database_organization_id" {
  description = "database_organization_id"
  type        = string
}
variable "database_project_name" {
  description = "database_project_name"
  type        = string
}
variable "database_provider" {
  default     = "AWS"
  description = "database_provider"
  type        = string
}
variable "database_credentials_user" {
  description = "database_credentials_user"
  type        = string
}
variable "database_region" {
  description = "database_region"
  type        = string
}
variable "database_type" {
  default     = "M0"
  description = "database_type"
  type        = string
}
variable "database_version" {
  description = "database_version"
  type        = string
}
variable "database_ip_access" {
  type        = string
  description = "database_ip_access"
}

variable "zone" {
  description = "zone"
  type        = string
}

variable "mongodb_atlas_public_key" {
  description = "mongodb_atlas_public_key"
  type        = string
}
variable "mongodb_atlas_private_key" {
  description = "mongodb_atlas_private_key"
  type        = string
}
