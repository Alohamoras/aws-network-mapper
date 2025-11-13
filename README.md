# AWS Network Mapper

A Python tool to collect and document AWS networking configurations in an easy-to-read markdown format.

## Features

- Collects comprehensive AWS networking information including:
  - VPCs, Subnets, Route Tables
  - Internet Gateways, NAT Gateways, Transit Gateways, VPN Gateways
  - Security Groups and Network ACLs
  - VPC Peering Connections
  - VPC Endpoints
  - Direct Connect configurations
- Outputs formatted markdown tables for easy documentation
- Supports multiple AWS regions and profiles

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Configure AWS credentials:
```bash
aws configure
```

## Usage

Basic usage (uses default region us-east-1):
```bash
python aws_network_mapper.py
```

Specify a region:
```bash
python aws_network_mapper.py --region us-west-2
```

Use a specific AWS profile:
```bash
python aws_network_mapper.py --profile my-profile
```

Specify custom output file:
```bash
python aws_network_mapper.py --output my-network-config.md
```

Full example:
```bash
python aws_network_mapper.py --region us-east-1 --profile production --output prod-network.md
```

## Output

The tool generates a markdown file containing:
- VPC configurations with CIDR blocks
- Subnet details with availability zones and IP counts
- Route table configurations with key routes
- Gateway configurations (IGW, NAT, TGW, VGW)
- Security group rules
- Network ACL configurations
- VPC peering connections
- VPC endpoints
- Direct Connect configurations (if available)

## AWS Permissions Required

The tool requires read-only permissions for:
- `ec2:Describe*` (VPCs, Subnets, Route Tables, Security Groups, etc.)
- `directconnect:Describe*` (Direct Connect resources)
- `sts:GetCallerIdentity` (to get account ID)

## Next Steps

After collecting your network configuration, you can:
1. Review the output for documentation purposes
2. Use AI tools to analyze the configuration and identify potential issues
3. Share with team members for review and planning
4. Track configuration changes over time by running periodically

## Project Structure

- `aws_network_mapper.py` - Main script for data collection
- `markdown_formatter.py` - Formats AWS data into markdown tables
- `requirements.txt` - Python dependencies
- `CLAUDE.md` - Documentation for AI assistants working with this codebase
