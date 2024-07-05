resource "aws_autoscaling_policy" "alb_policy_scale_up" {
  name                   = "${local.slug}-policy-scale-up"
  scaling_adjustment     = 1
  adjustment_type        = "ChangeInCapacity"
  cooldown               = 300
  autoscaling_group_name = aws_autoscaling_group.instances.name
}
resource "aws_cloudwatch_metric_alarm" "alb_metrics_cpu_utilization_high" {
  alarm_name          = "${local.slug}-metrics-cpu-utilization-high"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "60"
  statistic           = "Average"
  threshold           = var.instance_metrics_cpu_utilization_high_threshold
  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.instances.name
  }
  alarm_actions = [
    aws_autoscaling_policy.alb_policy_scale_up.arn,
  ]
}

resource "aws_autoscaling_policy" "alb_policy_scale_down" {
  name                   = "${local.slug}-policy-scale-down"
  scaling_adjustment     = -1
  adjustment_type        = "ChangeInCapacity"
  cooldown               = 300
  autoscaling_group_name = aws_autoscaling_group.instances.name
}
resource "aws_cloudwatch_metric_alarm" "alb_metrics_cpu_utilization_low" {
  alarm_name          = "${local.slug}-metrics-cpu-utilization-low"
  comparison_operator = "LessThanOrEqualToThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "60"
  statistic           = "Average"
  threshold           = var.instance_metrics_cpu_utilization_low_threshold
  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.instances.name
  }
  alarm_actions = [
    aws_autoscaling_policy.alb_policy_scale_down.arn,
  ]
}
