stage = "main"

main = "seek.demo.pe"

name     = "seek.demo.pe"
static   = "static-seek.demo.pe"

image_name  = "debian-12-amd64-*"
image_owner = "136693071363"

instance_type      = "t3.micro"
instance_disk_size = 50

instance_user         = "cristhian"
instance_key_name     = "seek.demo.pe"
instance_health_check = "/ping/"

instances_scale_desired                         = 1
instances_scale_min                             = 1
instances_scale_max                             = 1
instance_metrics_cpu_utilization_high_threshold = 80
instance_metrics_cpu_utilization_low_threshold  = 20
instances_metrics_healthy_hosts_threshold       = 1
instances_metrics_http_server_errors_threshold  = 100
instances_metrics_http_response_time_threshold  = 60

database_organization_id  = "66869c11aac7e32b4334a772"
database_project_name     = "seek-demo-pe"
database_credentials_user = "api"
database_region           = "US_EAST_1"
database_type             = "M10"
database_version          = "7.0"
database_ip_access        = "0.0.0.0/0"

files_static = "./files-static"

zone = "demo.pe"
