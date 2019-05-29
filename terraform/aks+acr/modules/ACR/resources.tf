resource "null_resource" "depends_on" {
  triggers {
    depends_on = "${join("", var.depends_on)}"
  }
}

resource "azurerm_container_registry" "acr" {
  name                = "${var.registry_name}"
  resource_group_name = "${var.resource_group_name}"
  location            = "${var.location}"
  sku                 = "${var.registry_type}"

  depends_on = [
    "null_resource.depends_on",
  ]
}
