# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AWS Network Mapper is a tool designed to collect and document AWS networking configurations in an easy-to-read format. The tool queries AWS infrastructure using the AWS CLI or SDK to generate comprehensive network topology documentation.

## Project Goals

1. Create scripts to collect AWS networking details (VPCs, subnets, route tables, gateways, etc.)
2. Output data in readable, copy-friendly formats (markdown tables)
3. Enable evaluation and feedback on network configurations through AI analysis

## Current State

The project is in early development. The `Notes.md` file contains example output showing the desired format for network documentation.

## Example Output Structure

The target output format includes structured sections for:
- VPCs (with CIDR blocks, state, and default status)
- Subnets (with availability zones, IP counts, and types)
- Route Tables (with associated subnets and key routes)
- Internet/NAT/Transit/VPN Gateways
- Security Groups (with inbound rules)
- Network ACLs
- VPC Peering Connections
- VPC Endpoints
- Direct Connect configurations
- Transit Gateway configurations
- Network topology summaries

## AWS Services to Query

When implementing the collection script, focus on these AWS networking services:
- EC2 (VPCs, Subnets, Route Tables, Internet Gateways, NAT Gateways, Security Groups, Network ACLs)
- VPC Peering
- Transit Gateway
- Direct Connect
- VPN Gateway
- VPC Endpoints

## Output Format Guidelines

- Use markdown tables for structured data
- Include summary sections for topology overview
- Group related resources together
- Highlight key routing information and connectivity patterns
- Provide both detailed tables and high-level summaries
- Include state/status information for all resources

## Development Approach

When building scripts:
- Use AWS SDK (boto3 for Python) or AWS CLI
- Handle multi-region queries if needed
- Include proper error handling for missing permissions
- Format output as markdown for easy documentation
- Consider pagination for large result sets
- Add date/timestamp to output for version tracking
