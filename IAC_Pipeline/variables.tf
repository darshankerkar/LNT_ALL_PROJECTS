variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "staging_instance_count" {
  description = "Number of instances for staging environment"
  type        = number
  default     = 1
}
