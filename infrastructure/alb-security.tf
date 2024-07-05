resource "aws_security_group" "alb" {
  name        = "${local.slug}-alb"
  description = "${local.slug}-alb"
  vpc_id      = local.vpc_id

  ingress {
    protocol    = "tcp"
    from_port   = "80"
    to_port     = "80"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    protocol    = "tcp"
    from_port   = "443"
    to_port     = "443"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${local.slug}-alb"
    Stage       = var.stage
    Description = "${local.slug}-alb"
  }
}

resource "aws_security_group" "instances" {
  name        = "${local.slug}-instances"
  description = "${local.slug}-instances"
  vpc_id      = local.vpc_id

  ingress {
    protocol        = "tcp"
    from_port       = "22"
    to_port         = "22"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    protocol    = "tcp"
    from_port   = "80"
    to_port     = "80"
    security_groups = [aws_security_group.alb.id]
  }
  egress {
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${local.slug}-instances"
    Stage       = var.stage
    Description = "${local.slug}-instances"
  }
}
