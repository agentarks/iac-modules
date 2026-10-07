targetScope = 'resourceGroup'

module eventGrid '../../modules/event-grid/main.bicep' = {
  name: 'event-grid-contract-check'
  params: {
    name: 'evt-contract-check'
    location: 'eastus'
    tags: {
      tenant: 'test'
      environment: 'sandbox'
      owner: 'platform-team'
      'cost-center': 'engineering'
    }
  }
}

output id string = eventGrid.outputs.id
output name string = eventGrid.outputs.name
output endpoint string = eventGrid.outputs.endpoint
