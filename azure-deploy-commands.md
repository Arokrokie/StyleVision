# Azure App Service Deployment Commands

## 1. Login to Azure CLI
```bash
az login
```

## 2. Set your subscription
```bash
az account set --subscription "22c03a35-4d0a-444e-aabd-0c6c20709641"
```

## 3. Create Resource Group (if needed)
```bash
az group create --name stylevision_group --location "East US"
```

## 4. Create App Service Plan
```bash
az appservice plan create \
  --name stylevision-plan \
  --resource-group stylevision_group \
  --sku B1 \
  --is-linux
```

## 5. Create Web App
```bash
az webapp create \
  --resource-group stylevision_group \
  --plan stylevision-plan \
  --name stylevision \
  --runtime "PYTHON|3.11" \
  --deployment-local-git
```

## 6. Configure App Settings
```bash
az webapp config appsettings set \
  --resource-group stylevision_group \
  --name stylevision \
  --settings \
    SECRET_KEY="your-secret-key-here" \
    DEBUG="False" \
    ALLOWED_HOSTS="stylevision.azurewebsites.net" \
    DJANGO_SETTINGS_MODULE="hair_project.settings" \
    SCM_DO_BUILD_DURING_DEPLOYMENT="true" \
    ENABLE_ORYX_BUILD="true"
```

## 7. Set Startup Command
```bash
az webapp config set \
  --resource-group stylevision_group \
  --name stylevision \
  --startup-file "python startup.py && gunicorn hair_project.wsgi --bind 0.0.0.0:8000 --workers 1 --timeout 300"
```

## 8. Deploy from Local Git
```bash
# Get deployment credentials
az webapp deployment user set --user-name your-username --password your-password

# Get Git URL
az webapp deployment source config-local-git \
  --resource-group stylevision_group \
  --name stylevision

# Add Azure remote and push
git remote add azure https://your-username@stylevision.scm.azurewebsites.net/stylevision.git
git push azure main
```

## Alternative: Deploy from GitHub
```bash
az webapp deployment source config \
  --resource-group stylevision_group \
  --name stylevision \
  --repo-url https://github.com/yourusername/your-repo \
  --branch main \
  --manual-integration
```
