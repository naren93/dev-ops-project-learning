/*
$ terraform apply -var-file="testing.tfvars" 
Incase we are declaring variable only here and giving the value thru tfvars.
To auto-load tfvars we can also use `foo.auto.tfvars` as a naming convention...
*/
variable "my_imageId" {
    default = "ami-036f5574583e16426"
    description = "AMI ID being used to create the instance."
}

variable "my_instanceType" {
    default = "t2.micro"
}

variable "my_cidrBlock" {
    type = string   # for the value have a look at the terraform.tfvars file
}

variable "instanceTags" {
    type = object({
        Name = string
        foo = number
    })
}

variable "foobar" {
    type = list(number)
}

variable "name" {
    type = string  
}