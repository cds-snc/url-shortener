output "vpc_id" {
  description = "VPC Id"
  value       = module.url_shortener_vpc.vpc_id
}

output "private_subnet_ids" {
  description = "List of the URL Shortner VPC private subnet ids"
  value       = module.url_shortener_vpc.private_subnet_ids
}

output "api_security_group_id" {
  description = "Api security group Id"
  value       = aws_security_group.api.id
}
