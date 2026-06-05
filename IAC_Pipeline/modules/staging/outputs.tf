output "instance_ids" {
  description = "IDs of the created instances"
  value       = aws_instance.staging[*].id
}

output "instance_ips" {
  description = "Public IPs of the created instances"
  value       = aws_instance.staging[*].public_ip
}

output "security_group_id" {
  description = "ID of the security group"
  value       = aws_security_group.staging.id
}
