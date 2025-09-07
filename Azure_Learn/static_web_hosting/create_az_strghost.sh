# --- 1. Authenticate to Azure using Service Principal ---
echo "Attempting to connect to Azure using Service Principal..."
# Use --output none to suppress verbose login output in pipeline logs
$TENANT_ID='47bb4e16-f695-425b-830a-837b5d5556fa'
az login --service-principal --username "$SERVICE_PRINCIPAL_APP_ID" \
         --password "$SERVICE_PRINCIPAL_SECRET" \
         --tenant "$TENANT_ID" \
         --output none
echo "Successfully connected to Azure."

# --- 2. Create Resource Group ---
echo "Checking/Creating Resource Group '$RESOURCE_GROUP_NAME' in '$LOCATION'..."
if ! az group show --name "$RESOURCE_GROUP_NAME" --output none 2>/dev/null; then
    echo "Resource Group '$RESOURCE_GROUP_NAME' does not exist. Creating..."
    az group create --name "$RESOURCE_GROUP_NAME" --location "$LOCATION" --output none
    echo "Resource Group '$RESOURCE_GROUP_NAME' created."
else
    echo "Resource Group '$RESOURCE_GROUP_NAME' already exists."
fi

# --- 3. Create Storage Account ---
echo "Checking/Creating Storage Account '$STORAGE_ACCOUNT_NAME'..."
# Note: Storage account names must be globally unique and lowercase (handled by dynamic name)
if ! az storage account show --name "$STORAGE_ACCOUNT_NAME" --resource-group "$RESOURCE_GROUP_NAME" --output none 2>/dev/null; then
    echo "Storage Account '$STORAGE_ACCOUNT_NAME' does not exist. Creating..."
    az storage account create --name "$STORAGE_ACCOUNT_NAME" \
                              --resource-group "$RESOURCE_GROUP_NAME" \
                              --location "$LOCATION" \
                              --sku Standard_LRS \
                              --kind StorageV2 \
                              --output none
    echo "Storage Account '$STORAGE_ACCOUNT_NAME' created."
else
    echo "Storage Account '$STORAGE_ACCOUNT_NAME' already exists."
fi

# --- 4. Enable Static Website Hosting ---
echo "Enabling Static Website Hosting on '$STORAGE_ACCOUNT_NAME'..."
# The --output tsv is used to parse the output and check if it's enabled.
# az storage blob service-properties show command to get static website properties
STATIC_WEBSITE_STATUS=$(az storage blob service-properties show \
    --account-name "$STORAGE_ACCOUNT_NAME" \
    --query "staticWebsite.enabled" \
    --output tsv)

if [ "$STATIC_WEBSITE_STATUS" == "false" ]; then
    az storage blob service-properties update \
        --account-name "$STORAGE_ACCOUNT_NAME" \
        --static-website \
        --index-document "index.html" \
        --404-document "404.html" \
        --output none
    echo "Static Website Hosting enabled."
elif [ "$STATIC_WEBSITE_STATUS" == "true" ]; then
    echo "Static Website Hosting is already enabled."
else
    echo "Could not determine static website status, proceeding to enable/update."
    az storage blob service-properties update \
        --account-name "$STORAGE_ACCOUNT_NAME" \
        --static-website \
        --index-document "index.html" \
        --404-document "404.html" \
        --output none
    echo "Static Website Hosting ensured to be enabled."
fi
# --- 5. Generate and Upload index.html ---
LOCAL_HTML_FILE_PATH="index.html"
echo "Uploading '$LOCAL_HTML_FILE_PATH' to \$web container..."
az storage blob upload \
    --account-name "$STORAGE_ACCOUNT_NAME" \
    --container-name "\$web" \
    --file "$LOCAL_HTML_FILE_PATH" \
    --name "index.html" \
    --content-type "text/html" \
    --overwrite true \
    --output none
echo "$LOCAL_HTML_FILE_PATH uploaded successfully."
# --- 6. Output Static Website URL ---
echo -e "\n--- Deployment Complete ---"
# Get the web endpoint URL
WEB_ENDPOINT=$(az storage account show \
    --name "$STORAGE_ACCOUNT_NAME" \
    --resource-group "$RESOURCE_GROUP_NAME" \
    --query "primaryEndpoints.web" \
    --output tsv)

echo "Your static website is live at: $WEB_ENDPOINT"
echo "Please allow a few minutes for DNS propagation and caching if this is a new deployment."
