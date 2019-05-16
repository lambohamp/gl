output "EC2 Public DNS Name " {
  value = ["${aws_instance.web.public_dns}"]
}
