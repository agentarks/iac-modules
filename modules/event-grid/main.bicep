targetScope = 'resourceGroup'

@sealed()
@description('Organization tags required on every Event Grid topic.')
type EventGridTags = {
  tenant: string
  environment: string
  owner: string
  'cost-center': string
}

@description('Topic name: 3–50 lowercase letters, digits, or hyphens.')
@minLength(3)
@maxLength(50)
param name string

@description('Approved Azure region.')
param location 'eastus' | 'centralus'

@description('Required organization tags. Values come from trusted caller configuration.')
param tags EventGridTags

resource topic 'Microsoft.EventGrid/topics@2022-06-15' = {
  name: name
  location: location
  tags: tags
  properties: {
    inputSchema: 'CloudEventSchemaV1_0'
    publicNetworkAccess: 'Disabled'
  }
}

@description('Resource ID of the Event Grid topic.')
output id string = topic.id

@description('Event Grid topic name.')
output name string = topic.name

@description('HTTPS endpoint used by consumers to publish events. Public network access is disabled.')
output endpoint string = topic.properties.endpoint
