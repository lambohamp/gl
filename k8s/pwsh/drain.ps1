param([string]$resource,[string]$cluster,[string]$pool_name1,[string]$pool_name2,[int]$node1_count,[int]$node2_count,[string]$remove_node)

# Evict pods from the given node
kubectl drain $remove_node --ignore-daemonsets --force --delete-local-data

# Remove the given node
kubectl delete node $remove_node

# Scale in the given node pool
az aks nodepool scale --resource-group $resource --cluster-name $cluster --name $pool_name1 --node-count $node1_count

# Scale out the given pool
az aks nodepool scale --resource-group $resource --cluster-name $cluster --name $pool_name2 --node-count $node2_count
