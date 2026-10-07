targetScope = 'resourceGroup'

@sealed()
@description('Required organization tags from trusted caller configuration.')
type EventHubTags = {
  tenant: string
  environment: string
  owner: string
  'cost-center': string
}

@description('Globally unique namespace name. Use 6–50 lowercase letters, digits, or hyphens. Azure checks character rules and availability.')
@minLength(6)
@maxLength(50)
param namespaceName string

@description('Event Hub name. Use 1–256 characters.')
@minLength(1)
@maxLength(256)
param eventHubName string

@description('Approved Azure region.')
param location 'eastus' | 'centralus'

@description('Required organization tags.')
param tags EventHubTags

@description('Namespace SKU tier.')
@allowed([
  'Standard'
  'Premium'
])
param sku string

@description('Namespace messaging unit capacity.')
@allowed([
  1
  2
  4
  8
])
param capacity int

@description('Number of partitions for the Event Hub.')
@allowed([
  1
  2
  3
  4
  5
  6
  7
  8
  9
  10
  11
  12
  13
  14
  15
  16
  17
  18
  19
  20
  21
  22
  23
  24
  25
  26
  27
  28
  29
  30
  31
  32
])
param partitionCount int

@description('Message retention in days. Standard supports 1–7 days.')
@allowed([
  1
  2
  3
  4
  5
  6
  7
])
param messageRetentionDays int

resource namespace 'Microsoft.EventHub/namespaces@2024-01-01' = {
  name: namespaceName
  location: location
  tags: tags
  sku: {
    name: sku
    tier: sku
    capacity: capacity
  }
  properties: {
    disableLocalAuth: true
    minimumTlsVersion: '1.2'
  }
}

resource eventHub 'Microsoft.EventHub/namespaces/eventhubs@2024-01-01' = {
  parent: namespace
  name: eventHubName
  properties: {
    partitionCount: partitionCount
    messageRetentionInDays: messageRetentionDays
  }
}

@description('Namespace resource ID.')
output namespaceId string = namespace.id

@description('Namespace name.')
output namespaceName string = namespace.name

@description('Event Hub resource ID.')
output eventHubId string = eventHub.id

@description('Event Hub name.')
output eventHubName string = eventHub.name
