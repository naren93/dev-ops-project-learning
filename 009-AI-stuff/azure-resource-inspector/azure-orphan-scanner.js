#!/usr/bin/env node

/**
 * azure-orphan-scanner.js
 * Scans an Azure resource list JSON and flags:
 *  - Orphaned public IP addresses (Microsoft.Network/publicIPAddresses)
 *  - Unattached managed disks (Microsoft.Compute/disks)
 *
 * Zero external dependencies: uses built-in Node.js fs and path modules.
 */

const fs = require('fs');
const path = require('path');

function printHelp() {
  console.log(`
Azure Resource Waste Scanner CLI

Usage:
  node azure-orphan-scanner.js <path-to-resources.json> [options]

Options:
  --json          Output results as JSON
  --help, -h      Display this help message

Examples:
  node azure-orphan-scanner.js ./azure-resources.fixture.json
  node azure-orphan-scanner.js ./azure-resources.fixture.json --json
`);
}

function extractResourceGroup(id = '') {
  const match = id.match(/\/resourceGroups\/([^/]+)/i);
  return match ? match[1] : 'N/A';
}

function isPublicIp(resource) {
  const type = (resource.type || '').toLowerCase();
  return type === 'microsoft.network/publicipaddresses';
}

function isManagedDisk(resource) {
  const type = (resource.type || '').toLowerCase();
  return type === 'microsoft.compute/disks';
}

function isPublicIpOrphaned(resource) {
  const props = resource.properties || {};
  const hasIpConfig = Boolean(props.ipConfiguration && (props.ipConfiguration.id || Object.keys(props.ipConfiguration).length > 0));
  const hasNatGateway = Boolean(props.natGateway && (props.natGateway.id || Object.keys(props.natGateway).length > 0));
  return !hasIpConfig && !hasNatGateway;
}

function isDiskUnattached(resource) {
  const props = resource.properties || {};
  const diskState = (props.diskState || '').toLowerCase();
  const managedBy = props.managedBy;

  if (diskState) {
    return diskState === 'unattached' || diskState === 'reserved';
  }
  return !managedBy;
}

function scanResources(resources) {
  const orphanedIps = [];
  const unattachedDisks = [];

  for (const item of resources) {
    if (isPublicIp(item)) {
      if (isPublicIpOrphaned(item)) {
        orphanedIps.push({
          name: item.name || 'unnamed',
          resourceGroup: extractResourceGroup(item.id),
          ipAddress: item.properties?.ipAddress || 'Unassigned',
          location: item.location || 'N/A',
          id: item.id
        });
      }
    } else if (isManagedDisk(item)) {
      if (isDiskUnattached(item)) {
        unattachedDisks.push({
          name: item.name || 'unnamed',
          resourceGroup: extractResourceGroup(item.id),
          sizeGB: item.properties?.diskSizeGB ?? 'N/A',
          diskState: item.properties?.diskState || 'Unattached',
          location: item.location || 'N/A',
          id: item.id
        });
      }
    }
  }

  return { orphanedIps, unattachedDisks };
}

function main() {
  const args = process.argv.slice(2);

  if (args.includes('-h') || args.includes('--help') || args.length === 0) {
    printHelp();
    process.exit(args.length === 0 ? 1 : 0);
  }

  const asJson = args.includes('--json');
  const filePathArg = args.find(arg => !arg.startsWith('--') && !arg.startsWith('-'));

  if (!filePathArg) {
    console.error('Error: Please provide a path to an Azure resources JSON file.');
    printHelp();
    process.exit(1);
  }

  const resolvedPath = path.resolve(process.cwd(), filePathArg);

  if (!fs.existsSync(resolvedPath)) {
    console.error(`Error: File not found at "${resolvedPath}"`);
    process.exit(1);
  }

  let rawData;
  try {
    rawData = fs.readFileSync(resolvedPath, 'utf8');
  } catch (err) {
    console.error(`Error reading file: ${err.message}`);
    process.exit(1);
  }

  let parsed;
  try {
    parsed = JSON.parse(rawData);
  } catch (err) {
    console.error(`Error parsing JSON: ${err.message}`);
    process.exit(1);
  }

  // Handle either a bare array [ ... ] or an Azure CLI / Resource Graph wrapper { "value": [ ... ] } or { "data": [ ... ] }
  const resources = Array.isArray(parsed)
    ? parsed
    : (Array.isArray(parsed.value) ? parsed.value : (Array.isArray(parsed.data) ? parsed.data : null));

  if (!resources) {
    console.error('Error: Input JSON must be an array of resources or an object containing a "value" or "data" array.');
    process.exit(1);
  }

  const { orphanedIps, unattachedDisks } = scanResources(resources);

  if (asJson) {
    const output = {
      summary: {
        totalScanned: resources.length,
        orphanedPublicIPsCount: orphanedIps.length,
        unattachedDisksCount: unattachedDisks.length
      },
      orphanedPublicIPs: orphanedIps,
      unattachedDisks
    };
    console.log(JSON.stringify(output, null, 2));
    return;
  }

  console.log('==============================================');
  console.log('          AZURE RESOURCE ORPHAN SCANNER       ');
  console.log('==============================================');
  console.log(`Scanned File : ${resolvedPath}`);
  console.log(`Total Items  : ${resources.length}\n`);

  // Section 1: Orphaned Public IPs
  console.log(`🚩 Orphaned Public IPs (${orphanedIps.length}):`);
  if (orphanedIps.length === 0) {
    console.log('  None found.');
  } else {
    orphanedIps.forEach((pip, idx) => {
      console.log(`  ${idx + 1}. [${pip.name}]`);
      console.log(`     IP Address     : ${pip.ipAddress}`);
      console.log(`     Resource Group : ${pip.resourceGroup}`);
      console.log(`     Location       : ${pip.location}`);
      console.log(`     Resource ID    : ${pip.id}`);
    });
  }

  console.log('');

  // Section 2: Unattached Disks
  console.log(`🚩 Unattached Managed Disks (${unattachedDisks.length}):`);
  if (unattachedDisks.length === 0) {
    console.log('  None found.');
  } else {
    unattachedDisks.forEach((disk, idx) => {
      console.log(`  ${idx + 1}. [${disk.name}]`);
      console.log(`     Size           : ${disk.sizeGB} GB`);
      console.log(`     State          : ${disk.diskState}`);
      console.log(`     Resource Group : ${disk.resourceGroup}`);
      console.log(`     Location       : ${disk.location}`);
      console.log(`     Resource ID    : ${disk.id}`);
    });
  }

  console.log('\n==============================================');
  const totalOrphans = orphanedIps.length + unattachedDisks.length;
  if (totalOrphans > 0) {
    console.log(`⚠️  Action recommended: ${totalOrphans} idle resources found.`);
  } else {
    console.log('✅ No orphaned resources detected.');
  }
}

if (require.main === module) {
  main();
}

module.exports = {
  scanResources,
  isPublicIpOrphaned,
  isDiskUnattached,
  extractResourceGroup
};
