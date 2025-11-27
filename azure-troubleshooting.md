# Azure App Service Troubleshooting Guide

## 1. Check App Service Status
- Go to Azure Portal → Your App Service → Overview
- Check if the app is "Running" or "Stopped"
- If stopped, click "Start"

## 2. Check Deployment Slot Issue
The error shows a slot: `bucwahcqdccqgzca`
- Go to your App Service → Deployment slots
- Check if this slot exists or was deleted
- If using slots, make sure you're accessing the correct URL

## 3. Check Application Logs
- Go to App Service → Monitoring → Log stream
- Or App Service → Development Tools → Advanced Tools (Kudu)
- Check for startup errors or deployment issues

## 4. Verify Deployment
- Go to App Service → Deployment Center
- Check if code is properly deployed
- Look for any failed deployments

## 5. Test Different URLs
Try accessing:
- https://stylevision.azurewebsites.net (production)
- https://stylevision-bucwahcqdccqgzca.azurewebsites.net (if slot exists)

## 6. Check Configuration
- App Service → Configuration → Application settings
- Verify all required environment variables are set
- Check startup command is configured
