using '../main.bicep'

param name = 'evt-example-001'
param location = 'eastus'
param tags = {
  tenant: 'acme'
  environment: 'sandbox'
  owner: 'platform-team'
  'cost-center': 'engineering'
}
