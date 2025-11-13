"""
Markdown formatter for AWS Network Configuration data
"""

from typing import Dict, List, Any


class MarkdownFormatter:
    """Formats AWS networking data as markdown tables and sections."""

    @staticmethod
    def format_table(headers: List[str], rows: List[List[str]]) -> str:
        """Format data as a markdown table."""
        if not rows:
            return "_No resources found_\n"

        # Calculate column widths
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))

        # Build table
        lines = []

        # Header row
        header_row = "| " + " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers)) + " |"
        lines.append(header_row)

        # Separator row
        separator = "|-" + "-|-".join("-" * w for w in col_widths) + "-|"
        lines.append(separator)

        # Data rows
        for row in rows:
            data_row = "| " + " | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)) + " |"
            lines.append(data_row)

        return "\n".join(lines) + "\n"

    def format_vpcs(self, vpcs: List[Dict[str, Any]]) -> str:
        """Format VPC information."""
        headers = ["VPC ID", "Name", "CIDR Block", "State", "Default"]
        rows = []

        for vpc in vpcs:
            rows.append([
                vpc['VpcId'],
                vpc['Name'] or '(unnamed)',
                vpc['CidrBlock'],
                vpc['State'],
                'Yes' if vpc['IsDefault'] else 'No'
            ])

        return self.format_table(headers, rows)

    def format_subnets(self, subnets: List[Dict[str, Any]]) -> str:
        """Format subnet information."""
        headers = ["Subnet ID", "Name", "VPC", "CIDR Block", "AZ", "Available IPs", "Type"]
        rows = []

        for subnet in subnets:
            rows.append([
                subnet['SubnetId'],
                subnet['Name'] or '(unnamed)',
                subnet['VpcId'],
                subnet['CidrBlock'],
                subnet['AvailabilityZone'],
                str(subnet['AvailableIpAddressCount']),
                subnet['Type']
            ])

        return self.format_table(headers, rows)

    def format_route_tables(self, route_tables: List[Dict[str, Any]]) -> str:
        """Format route table information."""
        headers = ["Route Table ID", "Name", "VPC", "Associated Subnets", "Key Routes"]
        rows = []

        for rt in route_tables:
            name = rt['Name'] or '(unnamed)'
            if rt['IsMain']:
                name += ' (Main)'

            subnet_info = 'Main route table' if rt['IsMain'] and not rt['SubnetIds'] else ', '.join(rt['SubnetIds'][:3])
            if len(rt['SubnetIds']) > 3:
                subnet_info += f", (+{len(rt['SubnetIds']) - 3} more)"

            key_routes = '; '.join(rt['KeyRoutes'][:3]) if rt['KeyRoutes'] else 'Local only'
            if len(rt['KeyRoutes']) > 3:
                key_routes += f" (+{len(rt['KeyRoutes']) - 3} more)"

            rows.append([
                rt['RouteTableId'],
                name,
                rt['VpcId'],
                subnet_info,
                key_routes
            ])

        return self.format_table(headers, rows)

    def format_internet_gateways(self, igws: List[Dict[str, Any]]) -> str:
        """Format Internet Gateway information."""
        headers = ["IGW ID", "Name", "State", "Attached VPC"]
        rows = []

        for igw in igws:
            rows.append([
                igw['InternetGatewayId'],
                igw['Name'] or '(unnamed)',
                igw['State'],
                igw['AttachedVpc']
            ])

        return self.format_table(headers, rows)

    def format_nat_gateways(self, nat_gws: List[Dict[str, Any]]) -> str:
        """Format NAT Gateway information."""
        headers = ["NAT Gateway ID", "Name", "VPC", "Subnet", "State", "Public IP", "Private IP"]
        rows = []

        for nat in nat_gws:
            rows.append([
                nat['NatGatewayId'],
                nat['Name'] or '(unnamed)',
                nat['VpcId'],
                nat['SubnetId'],
                nat['State'],
                nat['PublicIp'],
                nat['PrivateIp']
            ])

        return self.format_table(headers, rows)

    def format_transit_gateways(self, tgws: List[Dict[str, Any]]) -> str:
        """Format Transit Gateway information."""
        headers = ["TGW ID", "Name", "State", "ASN", "Default Route Table"]
        rows = []

        for tgw in tgws:
            rows.append([
                tgw['TransitGatewayId'],
                tgw['Name'] or '(unnamed)',
                tgw['State'],
                str(tgw['AmazonSideAsn']),
                tgw['DefaultRouteTableId']
            ])

        return self.format_table(headers, rows)

    def format_vpn_gateways(self, vgws: List[Dict[str, Any]]) -> str:
        """Format VPN Gateway information."""
        headers = ["VGW ID", "Name", "State", "Type", "ASN", "Attached VPC"]
        rows = []

        for vgw in vgws:
            rows.append([
                vgw['VpnGatewayId'],
                vgw['Name'] or '(unnamed)',
                vgw['State'],
                vgw['Type'],
                str(vgw['AmazonSideAsn']),
                vgw['AttachedVpc']
            ])

        return self.format_table(headers, rows)

    def format_security_groups(self, sgs: List[Dict[str, Any]], limit: int = 20) -> str:
        """Format Security Group information (limited to most relevant)."""
        headers = ["SG ID", "Name", "VPC", "Key Inbound Rules"]
        rows = []

        # Show only first N security groups
        for sg in sgs[:limit]:
            inbound = '; '.join(sg['InboundRules'][:3]) if sg['InboundRules'] else 'None'
            if len(sg['InboundRules']) > 3:
                inbound += f" (+{len(sg['InboundRules']) - 3} more)"

            rows.append([
                sg['GroupId'],
                sg['GroupName'],
                sg['VpcId'],
                inbound
            ])

        result = self.format_table(headers, rows)

        if len(sgs) > limit:
            result += f"\nNote: There are {len(sgs)} total security groups. The table above shows the first {limit}.\n"

        return result

    def format_network_acls(self, nacls: List[Dict[str, Any]]) -> str:
        """Format Network ACL information."""
        headers = ["NACL ID", "VPC", "Subnets", "Type", "Rules"]
        rows = []

        for nacl in nacls:
            subnet_count = len(nacl['SubnetIds'])
            subnet_info = f"{subnet_count} subnet{'s' if subnet_count != 1 else ''}"

            rules = "Allow all inbound/outbound" if nacl['IsDefault'] else "Custom rules"

            rows.append([
                nacl['NetworkAclId'],
                nacl['VpcId'],
                subnet_info,
                nacl['Type'],
                rules
            ])

        result = self.format_table(headers, rows)
        result += "\nNote: All NACLs follow standard rule format (Rule 100: Allow all, Rule 32767: Deny all as default).\n"

        return result

    def format_vpc_peering(self, peerings: List[Dict[str, Any]]) -> str:
        """Format VPC Peering Connection information."""
        headers = ["Peering Connection ID", "Name", "Requester VPC", "Accepter VPC", "Status"]
        rows = []

        for peer in peerings:
            rows.append([
                peer['VpcPeeringConnectionId'],
                peer['Name'] or '(unnamed)',
                peer['RequesterVpc'],
                peer['AccepterVpc'],
                peer['Status']
            ])

        return self.format_table(headers, rows)

    def format_vpc_endpoints(self, endpoints: List[Dict[str, Any]]) -> str:
        """Format VPC Endpoint information."""
        headers = ["Endpoint ID", "Name", "Type", "VPC", "Service", "State"]
        rows = []

        for endpoint in endpoints:
            # Shorten service name for readability
            service = endpoint['ServiceName'].replace('com.amazonaws.', '')

            rows.append([
                endpoint['VpcEndpointId'],
                endpoint['Name'] or '(unnamed)',
                endpoint['VpcEndpointType'],
                endpoint['VpcId'],
                service,
                endpoint['State']
            ])

        return self.format_table(headers, rows)

    def format_ec2_instances(self, instances: List[Dict[str, Any]]) -> str:
        """Format EC2 instance information."""
        headers = ["Instance ID", "Name", "Type", "State", "VPC", "Subnet", "Private IP", "Public IP", "NAT Instance"]
        rows = []

        for instance in instances:
            # Show only running, stopped, or stopping instances (skip terminated)
            if instance['State'] in ['terminated', 'terminating']:
                continue

            nat_indicator = 'Yes' if instance['IsNatInstance'] else 'No'

            rows.append([
                instance['InstanceId'],
                instance['Name'] or '(unnamed)',
                instance['InstanceType'],
                instance['State'],
                instance['VpcId'],
                instance['SubnetId'],
                instance['PrivateIpAddress'],
                instance['PublicIpAddress'],
                nat_indicator
            ])

        if not rows:
            return "_No EC2 instances found (excluding terminated instances)_\n"

        result = self.format_table(headers, rows)

        # Add note about NAT instances
        nat_instances = [i for i in instances if i['IsNatInstance'] and i['State'] not in ['terminated', 'terminating']]
        if nat_instances:
            result += f"\nNote: {len(nat_instances)} NAT instance(s) detected (source/destination check disabled).\n"

        return result

    def format_direct_connect(self, dx_data: Dict[str, Any]) -> str:
        """Format Direct Connect information."""
        output = []

        # Connections
        if dx_data['connections']:
            output.append("### Direct Connect Connections\n")
            headers = ["Connection ID", "Name", "State", "Location", "Bandwidth", "AWS Device"]
            rows = []
            for conn in dx_data['connections']:
                rows.append([
                    conn['connectionId'],
                    conn.get('connectionName', '(unnamed)'),
                    conn['connectionState'],
                    conn['location'],
                    conn['bandwidth'],
                    conn.get('awsDeviceV2', 'N/A')
                ])
            output.append(self.format_table(headers, rows))

        # Virtual Interfaces
        if dx_data['virtual_interfaces']:
            output.append("### Virtual Interfaces (VIFs)\n")
            headers = ["VIF ID", "Name", "Type", "VLAN", "State", "BGP Status", "Customer ASN"]
            rows = []
            for vif in dx_data['virtual_interfaces']:
                rows.append([
                    vif['virtualInterfaceId'],
                    vif.get('virtualInterfaceName', '(unnamed)'),
                    vif['virtualInterfaceType'],
                    str(vif['vlan']),
                    vif['virtualInterfaceState'],
                    vif.get('bgpStatus', 'N/A'),
                    str(vif.get('customerAsn', 'N/A'))
                ])
            output.append(self.format_table(headers, rows))

        # DX Gateways
        if dx_data['dx_gateways']:
            output.append("### Direct Connect Gateways\n")
            headers = ["DX Gateway ID", "Name", "State", "ASN"]
            rows = []
            for gw in dx_data['dx_gateways']:
                rows.append([
                    gw['directConnectGatewayId'],
                    gw.get('directConnectGatewayName', '(unnamed)'),
                    gw['directConnectGatewayState'],
                    str(gw['amazonSideAsn'])
                ])
            output.append(self.format_table(headers, rows))

        return "\n".join(output) if output else "_No Direct Connect resources found_\n"

    def format_all(self, data: Dict[str, Any]) -> str:
        """Format all collected data into a complete markdown document."""
        output = []

        # Header
        metadata = data['metadata']
        output.append("# AWS Network Configuration\n")
        output.append(f"**Region:** {metadata['region']}  ")
        output.append(f"**Date:** {metadata['date']}  ")
        output.append(f"**Account:** {metadata['account_id']}\n")
        output.append("---\n")

        # VPCs
        output.append("## VPCs\n")
        output.append(self.format_vpcs(data['vpcs']))

        # Subnets
        output.append("\n## Subnets\n")
        output.append(self.format_subnets(data['subnets']))

        # Route Tables
        output.append("\n## Route Tables\n")
        output.append(self.format_route_tables(data['route_tables']))

        # Internet Gateways
        output.append("\n## Internet Gateways\n")
        output.append(self.format_internet_gateways(data['internet_gateways']))

        # NAT Gateways
        output.append("\n## NAT Gateways\n")
        output.append(self.format_nat_gateways(data['nat_gateways']))

        # Transit Gateways
        output.append("\n## Transit Gateways\n")
        output.append(self.format_transit_gateways(data['transit_gateways']))

        # VPN Gateways
        output.append("\n## VPN Gateways\n")
        output.append(self.format_vpn_gateways(data['vpn_gateways']))

        # EC2 Instances
        output.append("\n## EC2 Instances\n")
        output.append(self.format_ec2_instances(data['ec2_instances']))

        # Security Groups
        output.append("\n## Security Groups\n")
        output.append(self.format_security_groups(data['security_groups']))

        # Network ACLs
        output.append("\n## Network ACLs\n")
        output.append(self.format_network_acls(data['network_acls']))

        # VPC Peering
        output.append("\n## VPC Peering Connections\n")
        output.append(self.format_vpc_peering(data['vpc_peering']))

        # VPC Endpoints
        output.append("\n## VPC Endpoints\n")
        output.append(self.format_vpc_endpoints(data['vpc_endpoints']))

        # Direct Connect
        if any(data['direct_connect'].values()):
            output.append("\n## Direct Connect Configuration\n")
            output.append(self.format_direct_connect(data['direct_connect']))

        return "".join(output)
