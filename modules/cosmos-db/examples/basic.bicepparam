using '../main.bicep'

param name = 'cosmosexample001'
param location = 'eastus'
param consistencyLevel = 'Session'
param tags = {
  tenant: 'acme'
  environment: 'sandbox'
  owner: 'platform-team'
  'cost-center': 'engineering'
}
