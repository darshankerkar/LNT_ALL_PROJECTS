output "staging_instance_ids" {
  description = "IDs of staging environment instances"
  value       = module.staging_env.instance_ids
}

output "staging_instance_ips" {
  description = "Public IPs of staging environment instances"
  value       = module.staging_env.instance_ips
}

output "staging_security_group_id" {
  description = "ID of staging security group"
  value       = module.staging_env.security_group_id
}
