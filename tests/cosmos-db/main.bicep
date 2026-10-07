targetScope = 'resourceGroup'

module cosmos '../../modules/cosmos-db/main.bicep' = {
  name: 'cosmos-db-contract-check'
  params: {
    name: 'cosmoscontractcheck'
    location: 'eastus'
    consistencyLevel: 'Session'
    tags: {
      tenant: 'test'
      environment: 'sandbox'
      owner: 'platform-team'
      'cost-center': 'engineering'
    }
  }
}

output id string = cosmos.outputs.id
output name string = cosmos.outputs.name
output documentEndpoint string = cosmos.outputs.documentEndpoint
