#!/usr/bin/env python3
import boto3

ecs = boto3.client('ecs')

cluster_name = input("Enter cluster name: ")
# cluster_name = "ec2"

def get_provider_info(cluster_name):
    response = ecs.describe_clusters(clusters=[cluster_name])
    return {
        'capacityProviders': response['clusters'][0]['capacityProviders'],
        'defaultCapacityProvider': response['clusters'][0]['defaultCapacityProviderStrategy']
    }

def add_fargate(cluster_name, provider_info):
    if 'FARGATE' not in provider_info['capacityProviders']:
        print("Adding FARGATE capacity provider to the cluster...")
        provider_info['capacityProviders'].append('FARGATE')
        provider_info['capacityProviders'].append('FARGATE_SPOT')
        response = ecs.put_cluster_capacity_providers(
            cluster=cluster_name,
            capacityProviders=provider_info['capacityProviders'],
            defaultCapacityProviderStrategy=provider_info['defaultCapacityProvider']
        )
    else:
        print("FARGATE capacity provider already exists in the cluster")

def remove_fargate(cluster_name, provider_info):
    if 'FARGATE' in provider_info['capacityProviders'] or 'FARGATE_SPOT' in provider_info['capacityProviders']:
        print("Removing FARGATE and FARGATE_SPOT capacity provider from the cluster...")
        provider_info['capacityProviders'].remove('FARGATE')
        provider_info['capacityProviders'].remove('FARGATE_SPOT')
        print(provider_info)
        response = ecs.put_cluster_capacity_providers(
            cluster=cluster_name,
            capacityProviders=provider_info['capacityProviders'],
            defaultCapacityProviderStrategy=[
                {
                    'capacityProvider': provider_info['capacityProviders'][0],
                    'weight': provider_info['defaultCapacityProvider'][0]['weight'],
                    'base': provider_info['defaultCapacityProvider'][0]['base']
                }
            ]
        )
    else:
        print("FARGATE capacity provider does not exist in the cluster")

if __name__ == "__main__":
    provider_info = get_provider_info(cluster_name)
    if 'FARGATE' not in provider_info['capacityProviders']:
        add_provider = input("Add FARGATE capacity provider to the cluster? (y/N): ")
        if not add_provider:
            add_provider = 'N'
        if add_provider.lower() == 'y':
            add_fargate(cluster_name, provider_info)
            print("FARGATE capacity provider added to the cluster")
        else:
            print("FARGATE capacity provider not added to the cluster")
    else:
        print("FARGATE capacity provider already exists in the cluster")
        remove_provider = input("Remove FARGATE capacity provider from the cluster? (y/N): ")
        if not remove_provider:
            remove_provider = 'N'
        if remove_provider.lower() == 'y':
            remove_fargate(cluster_name, provider_info)
            print("FARGATE capacity provider removed from the cluster")
        else:
            print("FARGATE capacity provider not removed from the cluster")

