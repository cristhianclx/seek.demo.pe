resource "aws_launch_configuration" "instances" {
  name_prefix = "${local.slug}-instances-"

  image_id                    = data.aws_ami.AMI.id
  instance_type               = var.instance_type
  security_groups             = [aws_security_group.instances.id]
  associate_public_ip_address = true
  enable_monitoring           = true

  key_name             = var.instance_key_name
  iam_instance_profile = aws_iam_instance_profile.profile.name

  user_data = templatefile("./instance-data.sh", {
    STAGE                         = var.stage,
    SSH_CONFIG                    = templatefile("./files/etc/ssh/sshd_config", {}),
    USER                          = var.instance_user,
    USER_SSH_CONFIG               = templatefile("./files/home/user/ssh/config", {}),
    NGINX_CONF                    = templatefile("./files/etc/nginx/nginx.conf", {}),
    NGINX_PROXY_PARAMS_CONF       = templatefile("./files/etc/nginx/proxy-params.conf", {}),
    NGINX_SITES_AVAILABLE_DEFAULT = templatefile("./files/etc/nginx/sites-available/default", {}),
  })

  root_block_device {
    volume_type = var.instance_disk_type
    volume_size = var.instance_disk_size
  }

  metadata_options {
    http_endpoint = "enabled"
    http_tokens   = "required"
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_autoscaling_group" "instances" {
  name = "${local.slug}-instances"

  desired_capacity          = var.instances_scale_desired
  min_size                  = var.instances_scale_min
  max_size                  = var.instances_scale_max
  health_check_grace_period = 300
  health_check_type         = "EC2"

  vpc_zone_identifier  = local.vpc_private_zone_ids
  launch_configuration = aws_launch_configuration.instances.name
  target_group_arns = [
    aws_alb_target_group.instances.arn,
  ]
  enabled_metrics = [
    "GroupMinSize",
    "GroupMaxSize",
    "GroupDesiredCapacity",
    "GroupInServiceInstances",
    "GroupTotalInstances",
  ]
  metrics_granularity = "1Minute"

  tag {
    key                 = "Name"
    value               = var.name
    propagate_at_launch = true
  }
  tag {
    key                 = "Stage"
    value               = var.stage
    propagate_at_launch = true
  }
  tag {
    key                 = "Description"
    value               = "${local.slug}-instances"
    propagate_at_launch = true
  }

  lifecycle {
    create_before_destroy = true
  }
  depends_on = [aws_launch_configuration.instances]
}
