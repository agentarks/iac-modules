using '../main.bicep'

param name = 'rg-example-platform'
param location = 'eastus'
param tags = {
  tenant: 'acme'
  environment: 'sandbox'
  owner: 'platform-team'
  'cost-center': 'engineering'
}
