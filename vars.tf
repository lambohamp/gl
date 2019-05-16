variable "region" {
  default = "us-east-2"
}

variable "instance_type" {
  default = "t2.micro"
}

variable "instance_name" {
  default = "NGINX"
}

variable "ami" {
  type = "map"

  default = {
    us-east-2 = "ami-0c55b159cbfafe1f0"
  }
}

variable "vpc_cidr" {
  default = "10.0.0.0/16"
}

variable "subnet_cidr" {
  default = "10.0.1.0/24"
}

variable "your_ip" {
  description = "Enter your IP address or enter 0.0.0.0/0 if you want the resource to be public"
}

variable "ec2_port" {
  default = "80"
}
