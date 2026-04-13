# Everything in your terraform file is a module -

# Resource specifies a single instance or object that needs to be erected. Wheras your terraform file where all your resources, data sources, and other variables exist is a module.

# Whenever you add a new module or make changes on an existing child module you need to initialize terraform (terraform init)

terraform {
    required_version = ">= 0.12"
}
provider "aws" {
    region = var.region
}

resource "aws_subnet" "webserver" {
    vpc_id = var.vpc_id
    cidr_block = var.cidr_block
}

resource "aws_instance" "webInstance" {
    ami = var.ami
    instance_type = var.instance_type
    subnet_id = aws_subnet.webserver.id
    tags = {
        Name = "${var.webServerName} Tuts whatever"
    }
}