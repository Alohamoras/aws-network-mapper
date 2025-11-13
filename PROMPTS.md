# AWS Network Analysis Prompts

This file contains AI prompts designed to analyze the output from the AWS Network Mapper tool and provide security assessments, architecture recommendations, and remediation guidance.

## Usage Workflow

1. **Collect Network Data**: Run the network mapper to generate your configuration file
   ```bash
   python3 aws_network_mapper.py --output my-network-config.md
   ```

2. **High-Level Assessment**: Copy Prompt 1 below into Claude/ChatGPT, then paste your network config file content

3. **Detailed Remediation**: After reviewing the assessment, use Prompt 2 with the specific findings you want to address

---

## Prompt 1: High-Level Security & Architecture Assessment

```
I need you to perform a comprehensive security and architecture assessment of my AWS network configuration. Please analyze the configuration below across these four areas:

1. **Security Vulnerabilities**: Overly permissive security groups, exposed resources, missing encryption, public access risks, insecure routing
2. **Architecture Best Practices**: High availability, redundancy, subnet design, routing optimization, proper use of AWS services
3. **Compliance & Standards**: CIS AWS Foundations Benchmark, AWS Well-Architected Framework principles
4. **Cost Optimization**: Unused resources, oversized instances, inefficient resource usage, potential savings

Please structure your response as follows:

### Executive Summary
- Overall risk score (Critical/High/Medium/Low)
- Top 3 most critical findings
- Quick statistics (# of issues by severity)

### Critical Issues (Immediate Action Required)
- List each critical finding with:
  - Issue title
  - Affected resources (IDs)
  - Risk description
  - Potential impact

### High Priority Issues
- Same format as critical

### Medium Priority Issues
- Same format as critical

### Low Priority Issues & Recommendations
- Same format as critical

### Informational / Best Practices
- Observations and suggestions for improvement

### Compliance Summary
- CIS AWS Foundations Benchmark findings
- Well-Architected Framework pillar assessments

### Cost Optimization Opportunities
- Estimated potential monthly savings
- Quick wins vs. strategic changes

---

**AWS Network Configuration:**

[PASTE YOUR NETWORK-CONFIG.MD CONTENT HERE]
```

---

## Prompt 2: Detailed Remediation Plan

**Note**: Use this prompt after running Prompt 1 to get detailed remediation steps for specific issues.

```
Based on the security and architecture assessment we just completed, I need detailed remediation plans for the issues we identified.

For each issue I specify, please provide:

1. **Remediation Steps**: Detailed step-by-step instructions
2. **AWS Console Instructions**: Click-by-click navigation if applicable
3. **AWS CLI Commands**: Ready-to-run commands with placeholders clearly marked
4. **Infrastructure as Code**: Terraform or CloudFormation examples where relevant
5. **Before/After Configuration**: Show what changes
6. **Verification Steps**: How to confirm the fix worked
7. **Effort Estimate**: Quick win (<30min), Moderate (hours), Complex (days)
8. **Risk/Impact**: Any potential service disruption or considerations

Please also provide:
- **Prioritized Implementation Roadmap**: Recommended order of operations
- **Rollback Plan**: How to undo changes if something goes wrong
- **Testing Strategy**: How to test in non-production first

---

**Issues to remediate:**

[LIST SPECIFIC FINDINGS FROM THE HIGH-LEVEL ASSESSMENT, e.g.:]
- Critical: Security group sg-xxxxx allows SSH (22) from 0.0.0.0/0
- High: No VPC Flow Logs enabled for vpc-xxxxx
- Medium: NAT Gateway redundancy - only 1 NAT in multi-AZ VPC
- Cost: Unused Internet Gateway igw-xxxxx in detached state

[OR REQUEST REMEDIATION FOR ALL ISSUES OF A SPECIFIC SEVERITY:]
- Please provide remediation for all Critical and High severity findings
```

---

## Prompt 3: Compliance-Specific Deep Dive (Optional)

Use this prompt for detailed compliance analysis against specific frameworks.

```
Please perform a detailed compliance assessment of my AWS network configuration against the following frameworks:

1. **CIS AWS Foundations Benchmark v1.5.0**
   - Focus on networking-related controls (sections 4.x and 5.x)
   - List compliant, non-compliant, and not-applicable controls
   - Provide evidence from the configuration

2. **AWS Well-Architected Framework**
   - Security Pillar (SEC03: Protect data in transit and at rest, SEC04: Apply security at all layers)
   - Reliability Pillar (REL02: Plan your network topology, REL03: Design your workload service architecture)
   - Performance Efficiency Pillar (PERF04: Select the networking solution)
   - Cost Optimization Pillar (COST05: Design your network to reduce cost)

3. **NIST Cybersecurity Framework** (if applicable to your organization)
   - Identify: Asset Management (ID.AM)
   - Protect: Protective Technology (PR.PT)

For each non-compliant control:
- Control ID and description
- Current configuration status
- Required configuration
- Remediation priority

---

**AWS Network Configuration:**

[PASTE YOUR NETWORK-CONFIG.MD CONTENT HERE]
```

---

## Tips for Best Results

1. **Be Specific**: When using Prompt 2, reference specific resource IDs from your assessment
2. **Iterative Approach**: Start with critical issues, verify fixes, then move to high priority
3. **Context Matters**: If you have specific compliance requirements or business constraints, mention them
4. **Test First**: Always test changes in a non-production environment first
5. **Document Changes**: Keep a record of what was changed and why
6. **Combine with Other Tools**: Use AWS Security Hub, Trusted Advisor, or GuardDuty findings alongside these prompts

## Example Follow-up Questions

After getting your assessment, you might ask:

- "Can you prioritize the security groups that need immediate attention?"
- "Show me the AWS CLI commands to enable VPC Flow Logs for all VPCs"
- "What's the recommended CIDR allocation strategy for my subnet expansion?"
- "How do I implement HA for my NAT instance setup?"
- "Compare the cost of NAT instances vs NAT Gateways for my traffic patterns"

## Customization

Feel free to modify these prompts to:
- Add organization-specific policies or standards
- Focus on particular AWS services you use heavily
- Include budget constraints or timeline requirements
- Reference your internal security baselines
