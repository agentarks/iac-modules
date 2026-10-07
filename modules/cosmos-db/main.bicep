targetScope = 'resourceGroup'

@sealed()
@description('Organization tags required on every Cosmos DB account.')
type CosmosTags = {
  tenant: string
  environment: string
  owner: string
  'cost-center': string
}

@description('Globally unique account name: 3–44 lowercase letters, digits, or hyphens. Azure enforces character rules and availability.')
@minLength(3)
@maxLength(44)
param name string

@description('Approved Azure region. Must be supplied explicitly.')
param location 'eastus' | 'centralus'

@description('Required organization tags. Values come from trusted application enrollment.')
param tags CosmosTags

@description('Default consistency level for the account.')
param consistencyLevel 'Session' | 'Strong' | 'BoundedStaleness' = 'Session'

resource account 'Microsoft.DocumentDB/databaseAccounts@2024-05-15' = {
  name: name
  location: location
  tags: tags
  kind: 'GlobalDocumentDB'
  properties: {
    databaseAccountOfferType: 'Standard'
    publicNetworkAccess: 'Disabled'
    disableLocalAuth: true
    minimalTlsVersion: 'Tls12'
    consistencyPolicy: {
      defaultConsistencyLevel: consistencyLevel
      maxIntervalInSeconds: 5
      maxStalenessPrefix: 100
    }
    locations: [
      {
        locationName: location
        failoverPriority: 0
        isZoneRedundant: false
      }
    ]
  }
}

@description('Resource ID of the Cosmos DB account.')
output id string = account.id

@description('Cosmos DB account name.')
output name string = account.name

@description('NoSQL document endpoint. Network access and data-plane authorization are provisioned separately.')
output documentEndpoint string = account.properties.documentEndpoint
