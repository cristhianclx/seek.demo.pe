resource "aws_cloudwatch_metric_alarm" "instances_metrics_healthy_hosts" {
  alarm_name          = "${local.slug}-alb-metrics-healthy-hosts"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = 2
  metric_name         = "HealthyHostCount"
  namespace           = "AWS/ApplicationELB"
  period              = 60
  statistic           = "Average"
  threshold           = var.instances_metrics_healthy_hosts_threshold
  dimensions = {
    TargetGroup  = aws_alb_target_group.instances.arn_suffix
    LoadBalancer = aws_alb.alb.arn_suffix
  }
}
resource "aws_cloudwatch_metric_alarm" "instances_metrics_http_server_errors" {
  alarm_name          = "${local.slug}-alb-metrics-http-server-errors"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 2
  metric_name         = "HTTPCode_Target_5XX_Count"
  namespace           = "AWS/ApplicationELB"
  period              = 60
  statistic           = "Average"
  threshold           = var.instances_metrics_http_server_errors_threshold
  dimensions = {
    TargetGroup  = aws_alb_target_group.instances.arn_suffix
    LoadBalancer = aws_alb.alb.arn_suffix
  }
}
resource "aws_cloudwatch_metric_alarm" "instances_metrics_http_response_time" {
  alarm_name          = "${local.slug}-alb-metrics-http-response-time"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 2
  metric_name         = "TargetResponseTime"
  namespace           = "AWS/ApplicationELB"
  period              = 60
  statistic           = "Average"
  threshold           = var.instances_metrics_http_response_time_threshold
  dimensions = {
    TargetGroup  = aws_alb_target_group.instances.arn_suffix
    LoadBalancer = aws_alb.alb.arn_suffix
  }
}
