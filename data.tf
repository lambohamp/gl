data "template_file" "ec2-launch-configuration-user-data" {
  template = "${file("user-data.tpl")}"
}
