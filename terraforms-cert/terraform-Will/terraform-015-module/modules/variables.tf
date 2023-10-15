variable "vpc_id" {
    type = string
    description = "vpc id"
}

variable "cidr_block" {
    type = string
    description = "Subnet Cidr block"
}

variable "webServerName" {
    type = string
    description = "name of whatever"
}

variable "ami" {
    type = string
    description = "AMI id that we plan on using"
}

variable "instance_type" {
    type = string
    description = "instance type"
}

variable "region" {
    type = string
    default = "us-west-2"
}