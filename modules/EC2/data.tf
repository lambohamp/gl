
data "template_file" "ec2-launch-configuration-user-data" {
  template = "${file("${path.module}/user-data.tpl")}"
}

