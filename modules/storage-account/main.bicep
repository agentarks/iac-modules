targetScope = 'resourceGroup'

@sealed()
@description('Organization tags required on every storage account.')
type StorageTags = {
  tenant: string
  environment: string
  owner: string
  'cost-center': string
}

@description('Globally unique account name: 3–24 lowercase letters or digits. Azure enforces character rules and availability.')
@minLength(3)
@maxLength(24)
param name string

@description('Approved Azure region. Must be supplied explicitly.')
param location 'eastus' | 'centralus'

@description('Required organization tags. Values come from trusted application enrollment.')
param tags StorageTags

resource account 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: name
  location: location
  tags: tags
  kind: 'StorageV2'
  sku: {
    name: 'Standard_LRS'
  }
  properties: {
    supportsHttpsTrafficOnly: true
    minimumTlsVersion: 'TLS1_2'
    allowSharedKeyAccess: false
    allowBlobPublicAccess: false
    publicNetworkAccess: 'Disabled'
    defaultToOAuthAuthentication: true
    allowCrossTenantReplication: false
    networkAcls: {
      bypass: 'None'
      defaultAction: 'Deny'
    }
    encryption: {
      keySource: 'Microsoft.Storage'
      services: {
        blob: {
          enabled: true
          keyType: 'Account'
        }
        file: {
          enabled: true
          keyType: 'Account'
        }
      }
    }
  }
}

@description('Resource ID of the storage account.')
output id string = account.id

@description('Storage account name.')
output name string = account.name

@description('Service endpoints. Network access and data-plane authorization are provisioned separately.')
output endpoints object = account.properties.primaryEndpoints
