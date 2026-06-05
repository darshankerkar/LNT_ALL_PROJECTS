variable "environment_name" {
  description = "Name of the environment"
  type        = string
}

variable "aws_region" {
  description = "AWS region"
  type        = string
}

variable "instance_count" {
  description = "Number of EC2 instances"
  type        = number
  default     = 1
}

variable "tags" {
  description = "Tags for resources"
  type        = map(string)
  default     = {}
}
