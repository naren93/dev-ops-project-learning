terraform {
    required_providers {
        aws = {
            source  = "hashicorp/aws"
            version = "~> 5.0"
        }
    }
}

provider "aws" {
    region = "us-east-2"
}

/*
variable "my-instance-type" {
    type = string # Optional
    default = "t2.micro" # Optional
    description = "my instance type should always be a free instance tier." # Optional
}
*/

locals {
    setup_name = "tuts"
    foobar = upper("ram")
    baz = local.setup_name
}

resource "aws_vpc" "myVPC" {
    cidr_block = var.my_cidrBlock
    tags = {
        Name = "myVPC01-${locals.setup_name}"
    }
}

data "aws_vpc" "myVPC01" {
    # default = true
    filter {
        name = "tag:Name"
        values = ["Tuts"]
    }
}

data "aws_ami" "name" {
    owners = ["self"]
    most_recent = true
} # Use as `aws_ami.name`

output "foo" {
    value = data.aws_vpc.myVPC01
}

resource "aws_subnet" "mySubnet01" {
    vpc_id = aws_vpc.myVPC.id
    cidr_block =  "10.0.1.0/24"
    tags = {
        Name = "mySubnet01-${locals.setup_name}"
    }
}

resource "aws_instance" "myInstance01" {
    subnet_id = aws_subnet.mySubnet01.id
    ami = var.my_imageId # Changes made here and re-applied will re-create the server
    instance_type = var.my_instanceType # Changes made here and re-applied would not lead to re-creation of server
    count = 2 # 0 means i dont want to create any resource
    tags = var.instanceTags
    /*{
        Name = "myInstance01" # Changes made here and re-applied would not lead to re-creation of server
        foo = "bar" # Changes made here and re-applied would not lead to re-creation of server
    }*/
}

# terraform init
# terraform plan
# terraform apply - Can be directly used since this also does the plan anyways.
# terraform apply -auto-approve
# terraform destroy

resource "aws_instance" "web" {
    for_each = {
        dev = "t2.micro"
        prod = "t2.micro"
    }
    ami = var.my_imageId
    instance_type = each.value
    tags = {
        Name = "Web-${each.key}"
    } # Count and FOR-EACH are not to be used inside the same resource at the same time. Terraform will not allow.
}

output "web-details" {
    value = aws_instance.web[*].private_ip
    sensitive = false
}

provider "aws" {
    alias = "east"
    region = "us-east-1"
}
resource "aws_instance" "web_east" {
    provider = aws.east
    ami = var.my_imageId # please add a valid ami
    instance_type = "t2.micro"
    tags = {
        Name = "Tuts Test ${local.baz}"
        foo = local.baz == "aaa" ? "yes" : "no" # Short hand if-else statement
        # Multi-line text with specific intendations -
        bar = <<EOT
            TESTING FOO 
        EOT
        # Multi-line text without specified intendations -
        baz = <<-EOT
            TESTING GOO
        EOT
        testing_if = "Hello, %{if var.name != "" }${var.name}%{ else }unnamed%{ endif }!"
        testingLoop = <<-EOT
            %{ for ip in aws.instance.myInstance.*.private_ip }
                server ${ip}
            %{ endfor }
        EOT
    }
    lifecycle {
        # create_before_destroy = true
        prevent_destroy = true
        ignore_changes = [ tags ]
    }
}
