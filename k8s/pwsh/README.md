<pre>
############# Description ###########

We have 2 node pools with 3 and 1 nodes respectively. 2 nodes out of 3 in the firts pool are tainted with 
nginx=no:NoSchedule to prevent pod to be scheduled there. The third one is tainted with nginx=yes:NoSchedule; 
that's why we add a corresponding toleration to the deployment manifest. 
The node in the second pool is cordoned for the same reason. Therefore, when we apply the deployment, 
all the pods are created within a single node.

The final goal is to evict all the pods from the node and schedule them to a new one.

############# USAGE ################

pwsh drain.ps1 -resource [] -cluster [] -pool_name1 [] -pool_name2 [] -node1_count [] -node2_count [] -remove_node []

-resource                   Name of the resource group in Azure<br/>
-cluster                    Name of the AKS cluster<br/>
-pool_name1                 Name of the node pool you want to remove the node from<br/>
-pool_name2                 Name of the node pool you want to add the node to<br/>
-node1_count                The number of nodes you'd like to set for the first node pool<br/>
-node2_count                The number of nodes you'd like to set for the second node pool<br/>
-remove_node                Name of the node you'd like to remove<br/>

</pre>
