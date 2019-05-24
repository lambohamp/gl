output "EC2_Public_DNS_Name" {
  value = ["${aws_instance.web.public_dns}"]
}
