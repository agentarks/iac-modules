targetScope = 'resourceGroup'

@sealed()
@description('Organization tags required on every web app.')
type WebAppTags = {
  tenant: string
  environment: string
  owner: string
  'cost-center': string
}

@description('Web app name. Azure enforces naming rules and availability.')
param name string

@description('Explicit name for the Linux App Service plan.')
param planName string

@description('Approved Azure region.')
param location 'eastus' | 'centralus'

@description('Required organization tags. Values come from trusted application enrollment.')
param tags WebAppTags

@description('App Service plan SKU.')
param sku 'P1v3' | 'P2v3' | 'P3v3' | 'B1' | 'B2' | 'B3'

@description('Python runtime version for the Linux web app.')
param pythonVersion '3.11' | '3.12'

resource plan 'Microsoft.Web/serverfarms@2023-12-01' = {
  name: planName
  location: location
  tags: tags
  kind: 'linux'
  sku: {
    name: sku
    tier: contains(['B1', 'B2', 'B3'], sku) ? 'Basic' : 'PremiumV3'
    size: sku
    capacity: 1
  }
  properties: {
    reserved: true
    perSiteScaling: false
  }
}

resource site 'Microsoft.Web/sites@2023-12-01' = {
  name: name
  location: location
  tags: tags
  kind: 'app,linux'
  properties: {
    serverFarmId: plan.id
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'PYTHON|${pythonVersion}'
      minTlsVersion: '1.2'
      ftpsState: 'Disabled'
      http20Enabled: true
      // Basic-tier plans reject alwaysOn; only Premium supports it.
      alwaysOn: contains(['P1v3', 'P2v3', 'P3v3'], sku)
    }
  }
}

@description('Resource ID of the web app.')
output id string = site.id

@description('Web app name.')
output name string = site.name

@description('Default public hostname for the web app.')
output defaultHostName string = site.properties.defaultHostName
