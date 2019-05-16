resource "aws_vpc" "vpc" {
  cidr_block           = "${var.vpc_cidr}"
  enable_dns_hostnames = true

  tags = {
    Name = "${var.instance_name}"
  }
}

resource "aws_subnet" "subnet" {
  vpc_id                  = "${aws_vpc.vpc.id}"
  cidr_block              = "${var.subnet_cidr}"
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.instance_name}"
  }
}

resource "aws_security_group" "ec2_sg" {
  vpc_id      = "${aws_vpc.vpc.id}"
  name        = "${var.instance_name}_EC2"
  description = "Allow inbound http traffic"

  ingress {
    from_port   = "${var.ec2_port}"
    to_port     = "${var.ec2_port}"
    protocol    = "tcp"
    cidr_blocks = ["${var.your_ip}"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_internet_gateway" "gw" {
  vpc_id = "${aws_vpc.vpc.id}"

  tags = {
    Name = "${var.instance_name}"
  }
}

resource "aws_route_table" "r" {
  vpc_id = "${aws_vpc.vpc.id}"

  tags = {
    Name = "${var.instance_name}"
  }
}

resource "aws_route" "internet_access" {
  route_table_id         = "${aws_route_table.r.id}"
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = "${aws_internet_gateway.gw.id}"
}

resource "aws_route_table_association" "association" {
  subnet_id      = "${aws_subnet.subnet.id}"
  route_table_id = "${aws_route_table.r.id}"
}

resource "aws_instance" "web" {
  ami           = "${lookup(var.ami, var.region)}"
  instance_type = "${var.instance_type}"
  subnet_id     = "${aws_subnet.subnet.id}"
  user_data     = "${data.template_file.ec2-launch-configuration-user-data.rendered}"

  security_groups = [
    "${aws_security_group.ec2_sg.id}",
  ]

  tags = {
    Name = "${var.instance_name}"
  }
}
