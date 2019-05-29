variable "resource_group_name" {
  default = "k8s"
}

variable "cluster_name" {
  default = "gltest"
}

variable "registry_name" {
  default = "devopsintern"
}

variable "registry_type" {
  default = "Basic"
}

variable "agent_count" {
  description = "Enter the number of nodes in a pool"
}

variable "instance_type" {
  default = "Standard_DS1_v2"
}

variable "location" {
  default = "East US"
}

variable "pool_name" {
  default = "nodepool1"
}

variable "client_id" {}

variable "client_secret" {}
