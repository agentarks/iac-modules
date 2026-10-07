targetScope = 'subscription'

module resourceGroup '../../modules/resource-group/main.bicep' = {
  name: 'resource-group-contract-check'
  params: {
    name: 'rg-contract-check'
    location: 'eastus'
    tags: {
      tenant: 'test'
      environment: 'sandbox'
      owner: 'platform-team'
      'cost-center': 'engineering'
    }
  }
}

output id string = resourceGroup.outputs.id
output name string = resourceGroup.outputs.name
output location string = resourceGroup.outputs.location
