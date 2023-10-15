output "vpc" {
    value = aws_vpc.myVPC
}

output "subnetDetails" {
    value = aws_subnet.mySubnet01
}

output "instance_ip" {
    value = aws_instance.myInstance01[*].private_ip # or instead of 0 give the index of the array
    # value = [for instance in aws_instance.myInstance01 : instance]private_ip
    # value = [for k,v in var.testing : upper(k)]
    # value = [for k,v in var.testing : upper(k) if k == "foo"]
    sensitive = false
}

output "foogoobar" {
    value = "tuts"
}
