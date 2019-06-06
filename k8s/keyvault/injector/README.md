- Install aad-pod-identity

non-RBAC

```
kubectl create -f https://raw.githubusercontent.com/Azure/aad-pod-identity/master/deploy/infra/deployment.yaml
```

RBAC

```
kubectl create -f https://raw.githubusercontent.com/Azure/aad-pod-identity/master/deploy/infra/deployment-rbac.yaml
```

- Create User Azure Identity (better use the same group your AKS cluster uses; typically this resource group is prefixed with 'MC_' string)

```
az identity create -g <resourcegroup> -n <managedidentity-resourcename>
```

e.g.

```
az identity create -g MC_k8s_gltest_eastus -n my-identity
```

- Assign permissions to new identity to ensure your Azure user identity has all the required permissions to read the keyvault instance and to access content within your key vault instance.

```
az role assignment create --role Reader --assignee <principalid> --scope /subscriptions/<subscriptionid>/resourcegroups/<resourcegroup>/providers/Microsoft.KeyVault/vaults/<keyvaultname>
```

e.g.

```
az role assignment create --role Reader --assignee bb044bdb-4378-424c-bedf-8ab934801b2f --scope /subscriptions/44bd1d98-b09d-428c-9591-47afbfe42d75/resourcegroups/k8s/providers/Microsoft.KeyVault/vaults/gltest
```

- Set policy to access secrets in your keyvault

```
az keyvault set-policy -n <keyvaultname> --secret-permissions get --spn <YOUR AZURE USER IDENTITY CLIENT ID>
```

e.g.

```
az keyvault set-policy -n gltest --secret-permissions get --spn e60d2068-5365-497a-889a-c5278c2f2a1a
```

- Add a new AzureIdentity for the new identity to your cluster

```yaml
apiVersion: "aadpodidentity.k8s.io/v1" 
kind: AzureIdentity 
metadata: 
  name: my-identity 
spec: 
  type: 0 
  ResourceID: /subscriptions/44bd1d98-b09d-428c-9591-47afbfe42d75/resourcegroups/MC_k8s_gltest_eastus/providers/Microsoft.ManagedIdentity/userAssignedIdentities/my-identity 
  ClientID: e60d2068-5365-497a-889a-c5278c2f2a1a
```
  
- Add a new AzureIdentityBinding for the new Azure identity to your cluster

```yaml
apiVersion: "aadpodidentity.k8s.io/v1" 
kind: AzureIdentityBinding 
metadata: 
  name: my-identity-binding 
spec: 
  AzureIdentity: my-identity 
  Selector: gl-akv
```
  
- Include the aadpodidbinding label matching the Selector value set in the previous step so that this pod will be assigned an identity

```yaml
metadata: 
  labels: 
    aadpodidbinding: gl-akv
 ```

- Install injector Using custom authentication with credential injection enabled

```
helm install spv-charts/azure-key-vault-env-injector --set customAuth.enabled=true --set customAuth.autoInject.enabled=true --set customAuth.autoInject.podIdentitySelector=gl-akv
```

- The Env Injector needs to be anabled for each namespace

```yaml
apiVersion: v1 
kind: Namespace 
metadata: 
  name: akv 
  labels: 
    azure-key-vault-env-injection: enabled
 ```
- Create AzureKeyVaultSecret resources references secrets in Azure Key Vault

```yaml
apiVersion: spv.no/v1alpha1 
kind: AzureKeyVaultSecret 
metadata: 
  name: my-azure-keyvault-secret 
  namespace: akv 
spec: 
  vault: 
    name: my-kv # name of key vault 
    object: 
      type: secret # object type 
      name: test-secret # name of the object
```
- Inject into applications using syntax below, referencing to the AzureKeyVaultSecret in 10.

```yaml
env:

    name: <name of environment variable> value: <name of AzureKeyVaultSecret>@azurekeyvault
```

- Apply the resources to Kubernetes
