############# USAGE ################

pwsh drain.ps1 -resource [] -cluster [] -pool_name1 [] -pool_name2 [] -node1_count [] -node2_count [] -remove_node []

-resource                   Name of the resource group in Azure
-cluster                    Name of the AKS cluster
-pool_name1                 Name of the node pool you want to remove the node from
-pool_name2                 Name of the node pool you want to add the node to
-node1_count                The number of nodes you'd like to set for the first node pool
-node2_count                The number of nodes you'd like to set for the second node pool
-remove_node                Name of the node you'd like to remove
