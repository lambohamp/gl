resource "null_resource" "depends_on" {
  triggers {
    depends_on = "${join("", var.depends_on)}"
  }
}

resource "azurerm_kubernetes_cluster" "k8s" {
  name                = "${var.cluster_name}"
  location            = "${var.location}"
  resource_group_name = "${var.resource_group_name}"
  dns_prefix          = "${var.cluster_name}-dns"

  agent_pool_profile {
    name    = "${var.pool_name}"
    count   = "${var.agent_count}"
    vm_size = "${var.instance_type}"
  }

  service_principal {
    client_id     = "${var.client_id}"
    client_secret = "${var.client_secret}"
  }

  depends_on = [
    "null_resource.depends_on",
  ]
}
