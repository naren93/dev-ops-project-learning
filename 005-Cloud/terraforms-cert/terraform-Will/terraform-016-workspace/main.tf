terraform {
	required_providers {
		aws = {
			source  = "hashicorp/aws"
			version = "~> 3.74"
		}
	}
}

provider "aws" {
	region  = var.region
}

locals {
	name = "${terraform.workspace}-instance"
}

resource "aws_instance" "main" {
	ami           = var.ami
	instance_type = var.instance_type

	tags = {
		Name = local.name
	}
}

# terraform init 
# terraform plan -var-file dev.tfvars
# terrform apply -var-file dev.tfvars
# terraform plan -var-file prod.tfvars
# terrform apply -var-file prod.tfvars

# terrform workspace show
# terrform workspace select prod
# terraform apply -var-file prod.tfvars -auto-approve

