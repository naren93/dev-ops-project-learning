[CmdletBinding(SupportsShouldProcess=$true)]
param(
    [Parameter(Mandatory=$true)]
    [string]$ServicePrincipalAppId,

    [Parameter(Mandatory=$true)]
    [string]$ServicePrincipalSecret,

    [Parameter(Mandatory=$true)]
    [string]$TenantId,

    [Parameter(Mandatory=$true)]
    [string]$Location,

    [Parameter(Mandatory=$true)]
    [string]$ResourceGroupName,

    [Parameter(Mandatory=$true)]
    [string]$StorageAccountName # Must be globally unique, lowercase, 3-24 chars
)

$ErrorActionPreference = "Stop" # Stop script on any non-terminating error

Write-Host "--- Starting Static Website Deployment ---"

# --- 1. Authenticate to Azure using Service Principal ---
Write-Host "Attempting to connect to Azure using Service Principal..."
try {
    Connect-AzAccount -ServicePrincipal -ApplicationId $ServicePrincipalAppId `
        -Credential (New-Object System.Management.Automation.PSCredential($ServicePrincipalAppId, (ConvertTo-SecureString $ServicePrincipalSecret -AsPlainText -Force))) `
        -TenantId $TenantId
    Write-Host "Successfully connected to Azure."
}
catch {
    Write-Error "Failed to connect to Azure: $($_.Exception.Message)"
    exit 1
}

# --- 2. Create Resource Group ---
Write-Host "Checking/Creating Resource Group '$ResourceGroupName' in '$Location'..."
try {
    $rg = Get-AzResourceGroup -Name $ResourceGroupName -Location $Location -ErrorAction SilentlyContinue
    if (-not $rg) {
        if ($PSCmdlet.ShouldProcess("Resource Group '$ResourceGroupName'", "Create")) {
            New-AzResourceGroup -Name $ResourceGroupName -Location $Location | Out-Null
            Write-Host "Resource Group '$ResourceGroupName' created."
        }
    } else {
        Write-Host "Resource Group '$ResourceGroupName' already exists."
    }
}
catch {
    Write-Error "Error creating/checking Resource Group: $($_.Exception.Message)"
    exit 1
}

# --- 3. Create Storage Account ---
Write-Host "Checking/Creating Storage Account '$StorageAccountName'..."
try {
    $storageAccount = Get-AzStorageAccount -ResourceGroupName $ResourceGroupName -Name $StorageAccountName -ErrorAction SilentlyContinue
    if (-not $storageAccount) {
        if ($PSCmdlet.ShouldProcess("Storage Account '$StorageAccountName'", "Create")) {
            $storageAccount = New-AzStorageAccount -ResourceGroupName $ResourceGroupName -Name $StorageAccountName `
                -Location $Location -SkuName Standard_LRS -Kind StorageV2 -ErrorAction Stop
            Write-Host "Storage Account '$StorageAccountName' created."
        }
    } else {
        Write-Host "Storage Account '$StorageAccountName' already exists."
        $storageAccount = Get-AzStorageAccount -ResourceGroupName $ResourceGroupName -Name $StorageAccountName -ErrorAction Stop # Ensure we have the object
    }
}
catch {
    Write-Error "Error creating/checking Storage Account: $($_.Exception.Message)"
    exit 1
}

# --- 4. Enable Static Website Hosting ---
Write-Host "Enabling Static Website Hosting on '$StorageAccountName'..."
try {
    # Check if static website is already enabled
    $staticWebsiteProps = $storageAccount.Context.BlobEndPoint.Replace($storageAccount.Context.BlobEndPoint.Host, $storageAccount.Context.BlobEndPoint.Host.Replace($storageAccount.StorageAccountName, $($storageAccount.StorageAccountName + '.web'))) # Get the web endpoint
    $staticWebsiteEnabled = $false
    try {
        $getProps = Get-AzStorageAccountStaticWebsite -Context $storageAccount.Context -ErrorAction Stop
        if ($getProps.Enabled) {
            $staticWebsiteEnabled = $true
            Write-Host "Static website hosting is already enabled."
        }
    }
    catch {
        # Error means it's not enabled, or other issue. We'll proceed to enable.
    }

    if (-not $staticWebsiteEnabled) {
        if ($PSCmdlet.ShouldProcess("Static Website Hosting for '$StorageAccountName'", "Enable")) {
            Enable-AzStorageStaticWebsite -Context $storageAccount.Context `
                -IndexDocument "index.html" `
                -ErrorDocument404Path "404.html" # Assuming you'll add one later, or can be omitted
            Write-Host "Static Website Hosting enabled."
        }
    }
}
catch {
    Write-Error "Error enabling Static Website Hosting: $($_.Exception.Message)"
    exit 1
}

# --- 5. Upload html file to Storage Account ---
Write-Host "Uploading 'index.html' to \$web container..."
try {
    Set-AzStorageBlobContent -Container "\$web" `
        -File $localHtmlFilePath `
        -Blob "index.html" `
        -Context $storageAccount.Context `
        -ContentType "text/html" `
        -Force # Overwrite if exists
    Write-Host "index.html uploaded successfully."
}
catch {
    Write-Error "Error uploading index.html: $($_.Exception.Message)"
    exit 1
}
finally {
    # Clean up the locally generated HTML file
    if (Test-Path $localHtmlFilePath) {
        Remove-Item -Path $localHtmlFilePath -Force -ErrorAction SilentlyContinue
        Write-Host "Cleaned up temporary file: '$localHtmlFilePath'."
    }
}
# --- 6. Output Static Website URL ---
Write-Host "`n--- Deployment Complete ---"
$staticWebsiteUrl = $storageAccount.PrimaryEndpoints.Web
Write-Host "Your static website is live at: $staticWebsiteUrl"
Write-Host "Please allow a few minutes for DNS propagation and caching if this is a new deployment."

# Output the URL as a variable for Jenkins (if using Jenkins Pipeline)
Write-Host "##vso[task.setvariable variable=StaticWebsiteUrl;isOutput=true]$staticWebsiteUrl"
