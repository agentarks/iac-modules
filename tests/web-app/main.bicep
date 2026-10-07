targetScope = 'resourceGroup'

module webApp '../../modules/web-app/main.bicep' = {
  name: 'web-app-contract-check'
  params: {
    name: 'webapp-contract-check'
    planName: 'plan-contract-check'
    location: 'eastus'
    tags: {
      tenant: 'test'
      environment: 'sandbox'
      owner: 'platform-team'
      'cost-center': 'engineering'
    }
    sku: 'P1v3'
    pythonVersion: '3.12'
  }
}

output id string = webApp.outputs.id
output name string = webApp.outputs.name
output defaultHostName string = webApp.outputs.defaultHostName
