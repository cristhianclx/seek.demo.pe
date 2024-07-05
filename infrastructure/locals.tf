locals {
  slug   = replace(var.name, ".", "-")
  main   = replace(var.main, ".", "-")
  static = replace(var.static, ".", "-")
  vpc_id = aws_default_vpc.main.id
  vpc_public_zone_ids = [
    aws_default_subnet.a.id,
    aws_default_subnet.b.id,
    aws_default_subnet.c.id,
  ]
  vpc_private_zone_ids = [
    aws_default_subnet.a.id,
    aws_default_subnet.b.id,
    aws_default_subnet.c.id,
  ]
}
