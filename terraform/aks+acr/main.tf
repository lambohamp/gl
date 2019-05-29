provider "azurerm" {
  version = "=1.28.0"
}

module "AKS" {
  source              = "./modules/AKS"
  cluster_name        = "${var.cluster_name}"
  pool_name           = "${var.pool_name}"
  agent_count         = "${var.agent_count}"
  instance_type       = "${var.instance_type}"
  client_id           = "${var.client_id}"
  client_secret       = "${var.client_secret}"
  location            = "${var.location}"
  resource_group_name = "${var.resource_group_name}"

  depends_on = ["${module.Resource_group.id}"]
}

module "ACR" {
  source              = "./modules/ACR"
  registry_name       = "${var.registry_name}"
  registry_type       = "${var.registry_type}"
  location            = "${var.location}"
  resource_group_name = "${var.resource_group_name}"

  depends_on = ["${module.Resource_group.id}"]
}

module "Resource_group" {
  source              = "./modules/Resource_Group"
  resource_group_name = "${var.resource_group_name}"
  location            = "${var.location}"
}
