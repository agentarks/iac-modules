targetScope = 'resourceGroup'

module eventHub '../../modules/event-hub/main.bicep' = {
  name: 'event-hub-contract-check'
  params: {
    namespaceName: 'ehcontractcheck001'
    eventHubName: 'events'
    location: 'eastus'
    tags: {
      tenant: 'test'
      environment: 'sandbox'
      owner: 'platform-team'
      'cost-center': 'engineering'
    }
    sku: 'Standard'
    capacity: 1
    partitionCount: 4
    messageRetentionDays: 1
  }
}

output namespaceId string = eventHub.outputs.namespaceId
output namespaceName string = eventHub.outputs.namespaceName
output eventHubId string = eventHub.outputs.eventHubId
output eventHubName string = eventHub.outputs.eventHubName
