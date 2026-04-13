# Execute certain things after the server has been built. We can also use configuration management tool. Use them as last resort.
# Not recommended by terraforms itself.

terraform {
	required_providers {
		aws = {
			source  = "hashicorp/aws"
			version = "~> 3.74"
		}
	}
}

provider "aws" {
    region = "us-west-2"  
}
resource "aws_instance" "web01" {
    ami = "ami-036f5574583e16426"
    instance_type = "t2.micro"
    key_name = "Ram"

    tags = {
        Name = "Tuts test"
    }
    # If we want to store the file in a different system use a differen `host`
    connection {
        type = "ssh"
        host = self.private_ip # "123.321.123.321"
        user = "ec2-user"
        private_key = file("/home/ec2-user/Downloads/ram.pem")
    }
    # To upload a file on the server -
    provisioner "file" {
        content = "Hello there"
        destination = "/home/ec2-user/tuts.txt"
    }
    provisioner "local-exec" {
        command = "echo ${self.private_ip} > instance-ip.txt"
    }
    # On a remote (external) machine - 
    provisioner "remote-exec" {
        # when = "destroy"
        # on_failure = continue / fail
        connection {
            type = "ssh"
            host = self.private_ip # "123.321.123.321"
            user = "ec2-user"
            private_key = file("/home/ec2-user/Downloads/ram.pem")
        }
        inline = [
            "touch /home/ec2-user/tuts-remote-exec.txt"
        ]
    }
}

output "ip" {
    value = aws_instance.web01.private_ip
}
