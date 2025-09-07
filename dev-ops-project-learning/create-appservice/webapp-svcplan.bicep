param appServicePlanName string = 'ram-b1-linux-plan'
param location string = resourceGroup().location
param vnetName string = 'ram-app-vnet'
param subnetName string = 'ram-app-subnet'

// --- Virtual Network and Subnet ---
// resource vnet 'Microsoft.Network/virtualNetworks@2023-09-01' = {
//   name: vnetName
//   location: location
//   properties: {
//     addressSpace: {
//       addressPrefixes: [
//         '10.0.0.0/16' // Define your VNet address space
//       ]
//     }
//     subnets: [
//       {
//         name: subnetName
//         properties: {
//           addressPrefix: '10.0.0.0/24' // Define your subnet address range
//         }
//       }
//     ]
//   }
// }

// --- App Service Plan (Linux B1) ---
resource appServicePlan 'Microsoft.Web/serverfarms@2022-03-01' = {
  name: appServicePlanName
  location: location
  sku: {
    name: 'B1' // Basic tier
    tier: 'Basic'
    size: 'B1'
  }
  kind: 'linux' // Specify Linux OS
  properties: {
    reserved: true // Required for Linux plans
  }
}

output appServicePlanId string = appServicePlan.id
// output vnetId string = vnet.id
// output subnetId string = vnet.properties.subnets[0].id // Output the ID of the first subne
