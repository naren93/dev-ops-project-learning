# terraform apply -var-file dev.tfvars
# TF_VAR_my_instanceType = "t2.micro" terraform apply
# terraform apply -var="my_instanceType=t2.large"

/*
Variable precedence -
1. Environmental variables < 2. terraform.tfvars < 3. terraform.tfvars.json < 4. *.auto.tfvars (or) *.auto.tfvars.json < 5. -var (or) -var-file options on the command line. 

*/

my_cidrBlock = "10.0.0.0/16"

instanceTags = {
    Name = "tuts-instance-${count.index}"
    foo = "${count.index}"
}

foobar = [1,2,3,4,5]   # ["foo", "bar", "goo", "car"]