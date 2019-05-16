provider "aws" {
  region = "${var.region}"
}

module "EC2" {
  source        = "./modules/EC2"
  region        = "${var.region}"
  instance_type = "${var.instance_type}"
  instance_name = "${var.instance_name}"
  ami           = "${var.ami}"
  vpc_cidr      = "${var.vpc_cidr}"
  subnet_cidr   = "${var.subnet_cidr}"
  your_ip       = "${var.your_ip}"
  ec2_port      = "${var.ec2_port}"
}
