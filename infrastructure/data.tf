resource "aws_default_vpc" "main" {
  tags = {
    Name = "vpc"
  }
}
resource "aws_default_subnet" "a" {
  availability_zone = "us-east-1a"
  tags = {
    Name = "vpc-a"
  }
}
resource "aws_default_subnet" "b" {
  availability_zone = "us-east-1b"
  tags = {
    Name = "vpc-b"
  }
}
resource "aws_default_subnet" "c" {
  availability_zone = "us-east-1c"
  tags = {
    Name = "vpc-c"
  }
}
resource "aws_default_subnet" "d" {
  availability_zone = "us-east-1d"
  tags = {
    Name = "vpc-d"
  }
}
resource "aws_default_subnet" "e" {
  availability_zone = "us-east-1e"
  tags = {
    Name = "vpc-e"
  }
}
resource "aws_default_subnet" "f" {
  availability_zone = "us-east-1f"
  tags = {
    Name = "vpc-f"
  }
}

data "aws_acm_certificate" "main" {
  domain   = var.zone
  statuses = ["ISSUED"]
}
data "aws_route53_zone" "main" {
  name         = var.zone
  private_zone = false
}
