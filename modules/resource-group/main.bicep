targetScope = 'subscription'

@sealed()
@description('Required organization tags. Values come from trusted caller configuration.')
type ResourceGroupTags = {
  tenant: string
  environment: string
  owner: string
  'cost-center': string
}

@description('Resource group name. Use 1–90 letters, digits, hyphens, underscores, parentheses, or periods. The name cannot end with a period.')
@minLength(1)
@maxLength(90)
param name string

@description('Approved Azure region. Must be supplied explicitly.')
param location 'eastus' | 'centralus'

@description('Required organization tags. Additional tag keys are rejected.')
param tags ResourceGroupTags

resource resourceGroup 'Microsoft.Resources/resourceGroups@2024-03-01' = {
  name: name
  location: location
  tags: tags
}

@description('Resource ID of the resource group.')
output id string = resourceGroup.id

@description('Resource group name.')
output name string = resourceGroup.name

@description('Azure region of the resource group.')
output location string = resourceGroup.location
