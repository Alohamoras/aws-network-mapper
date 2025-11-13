# AWS Network Mapper

A Python tool to collect and document AWS networking configurations in an easy-to-read markdown format.

## Features

- Collects comprehensive AWS networking information including:
  - VPCs, Subnets, Route Tables
  - Internet Gateways, NAT Gateways, Transit Gateways, VPN Gateways
  - EC2 Instances (with NAT instance detection)
  - Security Groups and Network ACLs
  - VPC Peering Connections
  - VPC Endpoints
  - Direct Connect configurations
- Outputs formatted markdown tables for easy documentation
- Supports multiple AWS regions and profiles
- Includes AI analysis prompts for security and architecture assessment

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
- EC2 instances with network details (identifies NAT instances)
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

## Analyzing Your Network Configuration

After collecting your network data, use the AI analysis prompts in `PROMPTS.md` to get:

1. **Security Assessment**: Identify vulnerabilities, overly permissive rules, and exposed resources
2. **Architecture Review**: Best practices for HA, redundancy, routing, and subnet design
3. **Compliance Analysis**: CIS AWS Foundations Benchmark and Well-Architected Framework alignment
4. **Cost Optimization**: Find unused resources and opportunities for savings

### Quick Start Analysis

```bash
# 1. Collect your network configuration
python aws_network_mapper.py --output my-network.md

# 2. Open PROMPTS.md and copy "Prompt 1: High-Level Assessment"

# 3. Paste the prompt into Claude or ChatGPT, followed by your network config content

# 4. Review findings and use "Prompt 2: Detailed Remediation" for specific issues
```

See [PROMPTS.md](PROMPTS.md) for detailed instructions and example prompts.

## Workflow

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Run Network    │────▶│  Review Output   │────▶│  AI Analysis    │
│     Mapper      │     │   (Markdown)     │     │   (Prompts)     │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                                                           │
                                                           ▼
                        ┌──────────────────┐     ┌─────────────────┐
                        │   Track Over     │◀────│   Implement     │
                        │      Time        │     │  Remediations   │
                        └──────────────────┘     └─────────────────┘
```

## Project Structure

- `aws_network_mapper.py` - Main script for data collection
- `markdown_formatter.py` - Formats AWS data into markdown tables
- `PROMPTS.md` - AI analysis prompts for security and architecture assessment
- `requirements.txt` - Python dependencies
- `CLAUDE.md` - Documentation for AI assistants working with this codebase
- `Notes.md` - Example output and project planning notes
