targetScope = 'resourceGroup'

module storage '../../modules/storage-account/main.bicep' = {
  name: 'storage-contract-check'
  params: {
    name: 'stcontractcheck001'
    location: 'eastus'
    tags: {
      tenant: 'test'
      environment: 'sandbox'
      owner: 'platform-team'
      'cost-center': 'engineering'
    }
  }
}

output id string = storage.outputs.id
output name string = storage.outputs.name
output endpoints object = storage.outputs.endpoints
