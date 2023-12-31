

# Tutorial

https://learn.microsoft.com/en-us/azure/app-service/tutorial-custom-container?tabs=azure-cli&pivots=container-linux



az group create --name containers-rg --location eastus

<!--is this needed here? or in the identity section below?
az identity create --name brianID --resource-group containers-rg
-->

az acr create --name registorium --resource-group containers-rg --sku Basic --admin-enabled true

az acr credential show --resource-group containers-rg --name registorium

(The JSON output of this command provides two passwords along with the registry's user name.)

    username is "registorium"
    password is "Yb72ZpxhUUuUnadLlz+3wqGmsGJEJpTLf9fVbHfxQZ+ACRBfE+2P"
    password2 is "DCgNAqCue5M/d+IqeES0wYnm9+kQOaqDap6OkHHRlv+ACRDa1of+"


(usename is, by default, the same as the registry name)

docker login registorium.azurecr.io --username registorium

(will ask for a password. Use one of the passwords from the previous step)

<!-- try the following

PASSWD=$(az acr credential show --resource-group containers-rg --name registorium --output tsv --query passwords[0].value)

docker login registorium.azurecr.io --username registorium --password-stdin <<< $PASSWD
-->

docker tag usermap registorium.azurecr.io/usermap:latest

docker push registorium.azurecr.io/usermap:latest



(create web app)

az group create --name webapp-rg --location eastus

az appservice plan create --name brian-web-app-plan --resource-group webapp-rg --is-linux
'
az webapp create --resource-group msdocs-custom-container-tutorial --plan myAppServicePlan --name usermapper0001 --deployment-container-image-name registorium.azurecr.io/usermap:latest

(configure app)

az webapp config appsettings set --resource-group webapp-rg --name usermapper0001 --settings WEBSITES_PORT=8080

https://usermapper0001.azurewebsites.net




NOTE: if access expires, is it renewed with the command:
az acr update --name registorium --admin-enabled true
?


try

az appservice plan create --name brian-web-app-plan --resource-group webapp-rg --is-linux

(configure app)

az webapp config appsettings set --resource-group webapp-rg --name usermapper0001 --settings WEBSITES_PORT=8080




# Troubleshooting

Turn on logs

az webapp log config --name usermapping0001 --resource-group webapp-rg --docker-container-logging filesystem

Get logs at:

https://usermapping0001.scm.azurewebsites.net/api/logs/docker





clean up
az group delete --name webapp-rg --no-wait --yes --verbose

















(the rest enables easy updates using CI/CD and web hook)

(create Principle)

principalId=$(az identity show --resource-group containers-rg --name brianID --query principalId --output tsv)

registryId=$(az acr show --resource-group containers-rg --name registorium --query id --output tsv)

az role assignment create --assignee $principalId --scope $registryId --role "AcrPull"

(enable identity)


id=$(az identity show --resource-group msdocs-custom-container-tutorial --name brianID --query id --output tsv)
az webapp identity assign --resource-group msdocs-custom-container-tutorial --name <app-name> --identities $id

(anable app to pull container)

appConfig=$(az webapp config show --resource-group msdocs-custom-container-tutorial --name <app-name> --query id --output tsv)
az resource update --ids $appConfig --set properties.acrUseManagedIdentityCreds=True

clientId=$(az identity show --resource-group msdocs-custom-container-tutorial --name brianID --query clientId --output tsv)
az resource update --ids $appConfig --set properties.AcrUserManagedIdentityID=$clientId














# Push image to a private repo

Because image contains secrets

<!--
```bash
$ docker tag usermap blinklet/usermap
$ docker login
$ docker push blinklet/usermap
```
-->

Azure OCI

https://learn.microsoft.com/en-us/azure/container-registry/container-registry-get-started-azure-cli

```
az login

az group create --location eastus --name artifactsRG

az acr create --resource-group artifactsRG \
  --name registorium --sku Standard
```

Login https://learn.microsoft.com/en-us/azure/container-registry/container-registry-authentication?tabs=azure-cli#individual-login-with-azure-ad

Login and get token (used for docker login later with admin user)
```
TOKEN=$(az acr login --name registorium --expose-token --output tsv --query accessToken)
```

Tag and push

```
docker tag usermap registorium.azurecr.io/usermap

docker push registorium.azurecr.io/usermap
```

List images

```
az acr repository list --name registorium --output table
```
```
Result
--------
usermap
```


# Run on ACI???

Azure Container Instances

https://docs.docker.com/cloud/aci-integration/

looks simple but is not in free tier. All contianer deployment options in Azure are discussed here, wrt to pricing
https://jussiroine.com/2021/12/running-a-single-docker-container-in-azure-cost-effectively/


# web app for containers

https://learn.microsoft.com/en-us/azure/app-service/quickstart-custom-container?tabs=dotnet&pivots=container-windows-cli


https://learn.microsoft.com/en-us/azure/devops/pipelines/apps/cd/deploy-docker-webapp?view=azure-devops&tabs=python%2Cyaml

```
az group create --name usermapRG --location eastus

az appservice plan create \
  --resource-group usermapRG \
  --location eastus \
  --name usermapPlan2 \
  --sku F1 \
  --is-linux
```

Need admin user to deploy container to app service
https://learn.microsoft.com/en-us/azure/container-registry/container-registry-authentication?tabs=azure-cli#admin-account


az acr update -n registorium --admin-enabled true

$ docker login registorium.azurecr.io --username 00000000-0000-0000-0000-000000000000 --password-stdin <<< $TOKEN



az webapp create \
  --name usermapApp \
  --plan usermapPlan \
  --resource-group usermapRG \
  --deployment-container-image-name registorium.azurecr.io/usermap
```

After deployment, your app is available at http://<app-name>.azurewebsites.net.

```
az webapp delete --name usermapApp --resource-group usermapRG
```

# Run on VPS

web apps are always free

https://learn.microsoft.com/en-us/training/modules/deploy-run-container-app-service/2-build-store-images

but, every service will do it differently. VPS's require more responsibility but work relativbely the same in most services.

However, this is the easiest way to securely assign secrets (VPS would need Docker Swarm or Kubernetes to securely inject environment variables at run time, which is overkill for our simple web app.)



or run on a VPS that is free for 12 months, about $5 per month after that

Azure B1s burstable VM

https://learn.microsoft.com/en-us/azure/virtual-machines/linux/quick-create-cli


<!--
securely deploy docker container to server

https://jfrog.com/devops-tools/article/3-steps-to-securing-your-docker-container-deployments/#:~:text=3%20Essential%20Steps%20to%20Securing%20Your%20Docker%20Container,3%203.%20Keep%20Your%20Images%20Lean%20and%20Clean

https://www.equalexperts.com/blog/tech-focus/quick-wins-to-secure-your-docker-containers/

https://stackoverflow.com/questions/39855304/how-to-add-user-with-dockerfile
-->


```
export RESOURCE_GROUP_NAME=usermapRG
export LOCATION=eastus
export VM_NAME=usermapVM
export VM_IMAGE=Ubuntu2204
export VM_SIZE=Standard_B1s
export ADMIN_USERNAME=usermap67

az group create --name $RESOURCE_GROUP_NAME --location $LOCATION

az vm create \
  --resource-group $RESOURCE_GROUP_NAME \
  --name $VM_NAME \
  --size $VM_SIZE
  --image $VM_IMAGE \
  --admin-username $ADMIN_USERNAME \
  --generate-ssh-keys \
  --public-ip-sku Standard

az vm run-command invoke \
   --resource-group $RESOURCE_GROUP_NAME \
   --name $VM_NAME \
   --command-id RunShellScript \
   --scripts "sudo apt-get update && sudo apt-get install -y nginx"


az vm open-port --port 80 --resource-group $RESOURCE_GROUP_NAME --name $VM_NAME

#### Get IP address

export IP_ADDRESS=$(az vm show --show-details --resource-group $RESOURCE_GROUP_NAME --name $VM_NAME --query publicIps --output tsv)

az group delete --name usermapRG --no-wait --yes --verbose




# Add domain name

https://learn.microsoft.com/en-us/azure/app-service/tutorial-secure-domain-certificate





on server, use sample compose file:

https://github.com/docker/awesome-compose/blob/master/nginx-wsgi-flask/compose.yaml




When the VM was created, teh Azure CLI created a network security group by default. List all services created in teh resource group so you can see their names:

```bash
$ az resource list -g vm-group -o table
Name                ResourceGroup    Location    Type                                     Status
------------------  ---------------  ----------  ---------------------------------------  --------
usermap-vm          vm-group         eastus      Microsoft.Compute/virtualMachines
usermap-vmVMNic     vm-group         eastus      Microsoft.Network/networkInterfaces
usermap-vmNSG       vm-group         eastus      Microsoft.Network/networkSecurityGroups
usermap-vmPublicIP  vm-group         eastus      Microsoft.Network/publicIPAddresses
usermap-vmVNET      vm-group         eastus      Microsoft.Network/virtualNetworks
```

Configure the Network Security group to allow only connections from your external IP address, on Port 80. You can see your external IP address by going to *google.com* and asking, "What is my IP address?".

```bash
az network nsg rule create \
  --resource-group vm-group \
  --nsg-name usermap-vmNSG \
  --name usermap-access-rule1 \
  --access Allow \
  --protocol Tcp \
  --direction Inbound \
  --priority 950 \
  --source-address-prefix 198.84.238.105 \
  --source-port-range "*" \
  --destination-port-range "80"
```