#!/usr/bin/env python3
"""
AWS Network Mapper - Collect and document AWS networking configurations
"""

import boto3
from datetime import datetime
from typing import Dict, List, Any
import sys
from markdown_formatter import MarkdownFormatter


class AWSNetworkMapper:
    """Collects AWS networking information and formats it as markdown."""

    def __init__(self, region: str = 'us-east-1', profile: str = None):
        """Initialize AWS clients for the specified region and profile."""
        session_args = {'region_name': region}
        if profile:
            session_args['profile_name'] = profile

        self.session = boto3.Session(**session_args)
        self.region = region
        self.ec2_client = self.session.client('ec2')
        self.dx_client = self.session.client('directconnect')

    def get_tag_value(self, tags: List[Dict], key: str) -> str:
        """Extract tag value from AWS tags list."""
        if not tags:
            return ''
        for tag in tags:
            if tag.get('Key') == key:
                return tag.get('Value', '')
        return ''

    def collect_vpcs(self) -> List[Dict[str, Any]]:
        """Collect VPC information."""
        print("Collecting VPCs...")
        response = self.ec2_client.describe_vpcs()
        vpcs = []

        for vpc in response.get('Vpcs', []):
            vpcs.append({
                'VpcId': vpc['VpcId'],
                'Name': self.get_tag_value(vpc.get('Tags', []), 'Name'),
                'CidrBlock': vpc['CidrBlock'],
                'State': vpc['State'],
                'IsDefault': vpc['IsDefault']
            })

        return vpcs

    def collect_subnets(self) -> List[Dict[str, Any]]:
        """Collect subnet information."""
        print("Collecting Subnets...")
        response = self.ec2_client.describe_subnets()
        subnets = []

        for subnet in response.get('Subnets', []):
            # Determine if subnet is public or private by checking route table
            subnet_type = 'Private'  # Default assumption

            subnets.append({
                'SubnetId': subnet['SubnetId'],
                'Name': self.get_tag_value(subnet.get('Tags', []), 'Name'),
                'VpcId': subnet['VpcId'],
                'CidrBlock': subnet['CidrBlock'],
                'AvailabilityZone': subnet['AvailabilityZone'],
                'AvailableIpAddressCount': subnet['AvailableIpAddressCount'],
                'Type': subnet_type
            })

        return subnets

    def collect_route_tables(self) -> List[Dict[str, Any]]:
        """Collect route table information."""
        print("Collecting Route Tables...")
        response = self.ec2_client.describe_route_tables()
        route_tables = []

        for rt in response.get('RouteTables', []):
            # Get associated subnets
            associations = rt.get('Associations', [])
            subnet_ids = [assoc['SubnetId'] for assoc in associations if 'SubnetId' in assoc]
            is_main = any(assoc.get('Main', False) for assoc in associations)

            # Format key routes
            routes = rt.get('Routes', [])
            key_routes = []
            for route in routes:
                dest = route.get('DestinationCidrBlock', route.get('DestinationPrefixListId', 'N/A'))

                if 'GatewayId' in route:
                    target = route['GatewayId']
                elif 'NatGatewayId' in route:
                    target = route['NatGatewayId']
                elif 'TransitGatewayId' in route:
                    target = route['TransitGatewayId']
                elif 'NetworkInterfaceId' in route:
                    target = route['NetworkInterfaceId']
                elif 'VpcPeeringConnectionId' in route:
                    target = route['VpcPeeringConnectionId']
                elif 'InstanceId' in route:
                    target = route['InstanceId']
                else:
                    target = 'local'

                state = route.get('State', 'active')
                if state == 'blackhole':
                    key_routes.append(f"{dest} → {target} (blackhole)")
                elif dest != route.get('DestinationCidrBlock') or target != 'local':
                    key_routes.append(f"{dest} → {target}")

            route_tables.append({
                'RouteTableId': rt['RouteTableId'],
                'Name': self.get_tag_value(rt.get('Tags', []), 'Name'),
                'VpcId': rt['VpcId'],
                'SubnetIds': subnet_ids,
                'IsMain': is_main,
                'KeyRoutes': key_routes
            })

        return route_tables

    def collect_internet_gateways(self) -> List[Dict[str, Any]]:
        """Collect Internet Gateway information."""
        print("Collecting Internet Gateways...")
        response = self.ec2_client.describe_internet_gateways()
        igws = []

        for igw in response.get('InternetGateways', []):
            attachments = igw.get('Attachments', [])
            attached_vpc = attachments[0]['VpcId'] if attachments else 'Not attached'
            state = attachments[0]['State'] if attachments else 'detached'

            igws.append({
                'InternetGatewayId': igw['InternetGatewayId'],
                'Name': self.get_tag_value(igw.get('Tags', []), 'Name'),
                'State': state,
                'AttachedVpc': attached_vpc
            })

        return igws

    def collect_nat_gateways(self) -> List[Dict[str, Any]]:
        """Collect NAT Gateway information."""
        print("Collecting NAT Gateways...")
        response = self.ec2_client.describe_nat_gateways()
        nat_gws = []

        for nat in response.get('NatGateways', []):
            addresses = nat.get('NatGatewayAddresses', [])
            public_ip = addresses[0].get('PublicIp', 'N/A') if addresses else 'N/A'
            private_ip = addresses[0].get('PrivateIp', 'N/A') if addresses else 'N/A'

            nat_gws.append({
                'NatGatewayId': nat['NatGatewayId'],
                'Name': self.get_tag_value(nat.get('Tags', []), 'Name'),
                'VpcId': nat['VpcId'],
                'SubnetId': nat['SubnetId'],
                'State': nat['State'],
                'PublicIp': public_ip,
                'PrivateIp': private_ip
            })

        return nat_gws

    def collect_transit_gateways(self) -> List[Dict[str, Any]]:
        """Collect Transit Gateway information."""
        print("Collecting Transit Gateways...")
        response = self.ec2_client.describe_transit_gateways()
        tgws = []

        for tgw in response.get('TransitGateways', []):
            options = tgw.get('Options', {})

            tgws.append({
                'TransitGatewayId': tgw['TransitGatewayId'],
                'Name': self.get_tag_value(tgw.get('Tags', []), 'Name'),
                'State': tgw['State'],
                'AmazonSideAsn': options.get('AmazonSideAsn', 'N/A'),
                'DefaultRouteTableId': options.get('AssociationDefaultRouteTableId', 'N/A')
            })

        return tgws

    def collect_vpn_gateways(self) -> List[Dict[str, Any]]:
        """Collect VPN Gateway information."""
        print("Collecting VPN Gateways...")
        response = self.ec2_client.describe_vpn_gateways()
        vgws = []

        for vgw in response.get('VpnGateways', []):
            attachments = vgw.get('VpcAttachments', [])
            attached_vpc = attachments[0]['VpcId'] if attachments else 'Not attached'

            vgws.append({
                'VpnGatewayId': vgw['VpnGatewayId'],
                'Name': self.get_tag_value(vgw.get('Tags', []), 'Name'),
                'State': vgw['State'],
                'Type': vgw['Type'],
                'AmazonSideAsn': vgw.get('AmazonSideAsn', 'N/A'),
                'AttachedVpc': attached_vpc
            })

        return vgws

    def collect_security_groups(self) -> List[Dict[str, Any]]:
        """Collect Security Group information."""
        print("Collecting Security Groups...")
        response = self.ec2_client.describe_security_groups()
        sgs = []

        for sg in response.get('SecurityGroups', []):
            # Summarize inbound rules
            inbound_rules = []
            for rule in sg.get('IpPermissions', [])[:5]:  # Limit to first 5 rules
                protocol = rule.get('IpProtocol', 'All')
                if protocol == '-1':
                    protocol = 'All'

                from_port = rule.get('FromPort', 'All')
                to_port = rule.get('ToPort', 'All')
                port_range = f"{from_port}" if from_port == to_port else f"{from_port}-{to_port}"

                # Get source
                sources = []
                for ip_range in rule.get('IpRanges', []):
                    sources.append(ip_range.get('CidrIp', ''))
                for sg_ref in rule.get('UserIdGroupPairs', []):
                    sources.append(sg_ref.get('GroupId', 'self'))

                source = ', '.join(sources) if sources else 'All'
                inbound_rules.append(f"{protocol}/{port_range} from {source}")

            sgs.append({
                'GroupId': sg['GroupId'],
                'GroupName': sg['GroupName'],
                'VpcId': sg.get('VpcId', 'EC2-Classic'),
                'InboundRules': inbound_rules
            })

        return sgs

    def collect_network_acls(self) -> List[Dict[str, Any]]:
        """Collect Network ACL information."""
        print("Collecting Network ACLs...")
        response = self.ec2_client.describe_network_acls()
        nacls = []

        for nacl in response.get('NetworkAcls', []):
            associations = nacl.get('Associations', [])
            subnet_ids = [assoc['SubnetId'] for assoc in associations]

            # Check if default
            is_default = nacl.get('IsDefault', False)
            nacl_type = 'Default' if is_default else 'Custom'

            nacls.append({
                'NetworkAclId': nacl['NetworkAclId'],
                'VpcId': nacl['VpcId'],
                'SubnetIds': subnet_ids,
                'Type': nacl_type,
                'IsDefault': is_default
            })

        return nacls

    def collect_vpc_peering(self) -> List[Dict[str, Any]]:
        """Collect VPC Peering Connection information."""
        print("Collecting VPC Peering Connections...")
        response = self.ec2_client.describe_vpc_peering_connections()
        peerings = []

        for peer in response.get('VpcPeeringConnections', []):
            requester = peer.get('RequesterVpcInfo', {})
            accepter = peer.get('AccepterVpcInfo', {})

            peerings.append({
                'VpcPeeringConnectionId': peer['VpcPeeringConnectionId'],
                'Name': self.get_tag_value(peer.get('Tags', []), 'Name'),
                'RequesterVpc': f"{requester.get('VpcId', 'N/A')} ({requester.get('CidrBlock', 'N/A')})",
                'AccepterVpc': f"{accepter.get('VpcId', 'N/A')} ({accepter.get('CidrBlock', 'N/A')})",
                'Status': peer['Status']['Code']
            })

        return peerings

    def collect_vpc_endpoints(self) -> List[Dict[str, Any]]:
        """Collect VPC Endpoint information."""
        print("Collecting VPC Endpoints...")
        response = self.ec2_client.describe_vpc_endpoints()
        endpoints = []

        for endpoint in response.get('VpcEndpoints', []):
            endpoints.append({
                'VpcEndpointId': endpoint['VpcEndpointId'],
                'Name': self.get_tag_value(endpoint.get('Tags', []), 'Name'),
                'VpcEndpointType': endpoint['VpcEndpointType'],
                'VpcId': endpoint['VpcId'],
                'ServiceName': endpoint['ServiceName'],
                'State': endpoint['State']
            })

        return endpoints

    def collect_ec2_instances(self) -> List[Dict[str, Any]]:
        """Collect EC2 instance information."""
        print("Collecting EC2 Instances...")
        response = self.ec2_client.describe_instances()
        instances = []

        for reservation in response.get('Reservations', []):
            for instance in reservation.get('Instances', []):
                # Get network interfaces info
                network_interfaces = instance.get('NetworkInterfaces', [])
                primary_eni = network_interfaces[0] if network_interfaces else {}

                # Determine if this is a NAT instance (source/dest check disabled)
                source_dest_check = instance.get('SourceDestCheck', True)
                is_nat_instance = not source_dest_check

                # Get security groups
                security_groups = [sg['GroupId'] for sg in instance.get('SecurityGroups', [])]

                instances.append({
                    'InstanceId': instance['InstanceId'],
                    'Name': self.get_tag_value(instance.get('Tags', []), 'Name'),
                    'InstanceType': instance['InstanceType'],
                    'State': instance['State']['Name'],
                    'VpcId': instance.get('VpcId', 'N/A'),
                    'SubnetId': instance.get('SubnetId', 'N/A'),
                    'PrivateIpAddress': instance.get('PrivateIpAddress', 'N/A'),
                    'PublicIpAddress': instance.get('PublicIpAddress', 'N/A'),
                    'PrimaryEniId': primary_eni.get('NetworkInterfaceId', 'N/A'),
                    'SecurityGroups': security_groups,
                    'IsNatInstance': is_nat_instance,
                    'SourceDestCheck': source_dest_check
                })

        return instances

    def collect_direct_connect(self) -> Dict[str, Any]:
        """Collect Direct Connect information."""
        print("Collecting Direct Connect configurations...")

        try:
            # Get connections
            connections = self.dx_client.describe_connections().get('connections', [])

            # Get virtual interfaces
            vifs = self.dx_client.describe_virtual_interfaces().get('virtualInterfaces', [])

            # Get Direct Connect gateways
            dx_gateways = self.dx_client.describe_direct_connect_gateways().get('directConnectGateways', [])

            return {
                'connections': connections,
                'virtual_interfaces': vifs,
                'dx_gateways': dx_gateways
            }
        except Exception as e:
            print(f"Warning: Could not collect Direct Connect info: {e}")
            return {'connections': [], 'virtual_interfaces': [], 'dx_gateways': []}

    def collect_all(self) -> Dict[str, Any]:
        """Collect all networking information."""
        print(f"\nCollecting AWS Network Configuration for region: {self.region}\n")

        return {
            'metadata': {
                'region': self.region,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'account_id': self.session.client('sts').get_caller_identity()['Account']
            },
            'vpcs': self.collect_vpcs(),
            'subnets': self.collect_subnets(),
            'route_tables': self.collect_route_tables(),
            'internet_gateways': self.collect_internet_gateways(),
            'nat_gateways': self.collect_nat_gateways(),
            'transit_gateways': self.collect_transit_gateways(),
            'vpn_gateways': self.collect_vpn_gateways(),
            'security_groups': self.collect_security_groups(),
            'network_acls': self.collect_network_acls(),
            'vpc_peering': self.collect_vpc_peering(),
            'vpc_endpoints': self.collect_vpc_endpoints(),
            'ec2_instances': self.collect_ec2_instances(),
            'direct_connect': self.collect_direct_connect()
        }


def main():
    """Main execution function."""
    import argparse

    parser = argparse.ArgumentParser(
        description='AWS Network Mapper - Collect and document AWS networking configurations'
    )
    parser.add_argument(
        '--region',
        default='us-east-1',
        help='AWS region to query (default: us-east-1)'
    )
    parser.add_argument(
        '--profile',
        help='AWS profile to use (default: default profile)'
    )
    parser.add_argument(
        '--output',
        default='network-config.md',
        help='Output file path (default: network-config.md)'
    )

    args = parser.parse_args()

    try:
        # Initialize mapper
        mapper = AWSNetworkMapper(region=args.region, profile=args.profile)

        # Collect data
        data = mapper.collect_all()

        print(f"\n✓ Data collection complete!")
        print(f"Total resources found:")
        print(f"  - VPCs: {len(data['vpcs'])}")
        print(f"  - Subnets: {len(data['subnets'])}")
        print(f"  - Route Tables: {len(data['route_tables'])}")
        print(f"  - Internet Gateways: {len(data['internet_gateways'])}")
        print(f"  - NAT Gateways: {len(data['nat_gateways'])}")
        print(f"  - Transit Gateways: {len(data['transit_gateways'])}")
        print(f"  - EC2 Instances: {len(data['ec2_instances'])}")
        print(f"  - Security Groups: {len(data['security_groups'])}")

        # Format to markdown
        print(f"\nFormatting output to markdown...")
        formatter = MarkdownFormatter()
        markdown_output = formatter.format_all(data)

        # Write to file
        with open(args.output, 'w') as f:
            f.write(markdown_output)

        print(f"\n✓ Network configuration written to: {args.output}")
        print(f"  File size: {len(markdown_output)} characters")

    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
