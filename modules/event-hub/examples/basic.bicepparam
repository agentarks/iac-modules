using '../main.bicep'

param namespaceName = 'eh-example-namespace-001'
param eventHubName = 'events'
param location = 'eastus'
param tags = {
  tenant: 'acme'
  environment: 'sandbox'
  owner: 'platform-team'
  'cost-center': 'engineering'
}
param sku = 'Standard'
param capacity = 1
param partitionCount = 4
param messageRetentionDays = 1
