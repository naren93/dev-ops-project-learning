# invoke-infra.ps1
param (
    [string]$ResourceGroupName,
    [string]$Location,
    [string]$TemplateFile,
    [string]$SubscriptionId,
    [string]$ClientId,
    [string]$ClientSecret,
    [string]$TenantId
)

Write-Host "--- Starting Azure Bicep Deployment ---"
Write-Host "Resource Group: $ResourceGroupName"
Write-Host "Location: $Location"
Write-Host "Template File: $TemplateFile"
Write-Host "Subscription ID: $SubscriptionId"

# Login to Azure using Service Principal
Write-Host "Attempting Azure login with Service Principal..."
try {
    az login --service-principal --username $ClientId --password $ClientSecret --tenant $TenantId --output none
    if ($LASTEXITCODE -ne 0) { throw "Azure login failed." }
    Write-Host "Azure login successful."
} catch {
    Write-Error "Failed to log in to Azure: $_"
    exit 1
}

# Set the active Azure subscription (good practice if SP has access to multiple)
Write-Host "Setting Azure subscription to: $SubscriptionId"
try {
    az account set --subscription $SubscriptionId --output none
    if ($LASTEXITCODE -ne 0) { throw "Setting subscription failed." }
    Write-Host "Subscription set successfully."
} catch {
    Write-Error "Failed to set subscription: $_"
    exit 1
}

# Create resource group if it doesn't exist
Write-Host "Checking for Resource Group: $ResourceGroupName in $Location"
$rgExists = az group show --name $ResourceGroupName --output tsv --query name 2>$null
if (-not $rgExists) {
    Write-Host "Resource Group '$ResourceGroupName' not found. Creating..."
    try {
        az group create --name $ResourceGroupName --location $Location --output none
        if ($LASTEXITCODE -ne 0) { throw "Resource group creation failed." }
        Write-Host "Resource Group '$ResourceGroupName' created successfully."
    } catch {
        Write-Error "Failed to create resource group: $_"
        exit 1
    }
} else {
    Write-Host "Resource Group '$ResourceGroupName' already exists."
}

# Deploy Bicep template
Write-Host "Deploying Bicep template '$TemplateFile' to resource group '$ResourceGroupName'..."
try {
    az deployment group create `
        --resource-group $ResourceGroupName `
        --template-file $TemplateFile `
        --parameters location=$Location `
        --output json # Output JSON for detailed logs in Jenkins
    
    if ($LASTEXITCODE -ne 0) { throw "Bicep deployment failed." }
    Write-Host "Bicep deployment successful."
} catch {
    Write-Error "Failed to deploy Bicep template: $_"
    exit 1
}

Write-Host "--- Azure Bicep Deployment Script Finished ---"