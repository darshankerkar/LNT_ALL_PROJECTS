terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

module "staging_env" {
  source = "./modules/staging"

  environment_name = "staging"
  aws_region       = var.aws_region
  instance_count   = var.staging_instance_count

  tags = {
    Environment = "staging"
    ManagedBy   = "Terraform"
    Project     = "CICD-Demo"
  }
}
