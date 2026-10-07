using '../main.bicep'

param name = 'acme-sandbox-web'
param planName = 'acme-sandbox-plan'
param location = 'eastus'
param tags = {
  tenant: 'acme'
  environment: 'sandbox'
  owner: 'platform-team'
  'cost-center': 'engineering'
}
param sku = 'P1v3'
param pythonVersion = '3.12'
