terraform {
  required_version = ">=1.9.1"

  backend "s3" {
    bucket               = "infrastructure.demo.pe"
    key                  = "seek.demo.pe"
    encrypt              = "true"
    region               = "sa-east-1"
    workspace_key_prefix = "tf"
  }
}
