# Terraform Infrastructure for Amazon Nova Sonic Call Center Agent

This Terraform configuration deploys the same infrastructure as the CDK version, but using Terraform modules for better organization and reusability.

## Architecture

This deployment creates:
- **Network Module**: VPC, subnets, NLB, CloudFront, S3
- **Compute Module**: ECS Fargate cluster and service
- **Auth Module**: Cognito User Pool and App Client
- **Frontend Module**: S3 bucket deployment and Lambda config generator

## Prerequisites

- Terraform >= 1.0
- AWS CLI configured
- Docker installed (for building container images)
- Node.js 20+ (for building frontend)
- Amazon Nova Sonic enabled in Bedrock (us-east-1)

## Directory Structure

```
terraform/
├── main.tf                 # Root module - orchestrates everything
├── variables.tf            # Input variables
├── outputs.tf              # Output values
├── terraform.tfvars        # Your variable values (create from template)
├── modules/
│   ├── network/           # VPC, NLB, CloudFront, S3
│   ├── compute/           # ECS Fargate
│   ├── auth/              # Cognito
│   └── frontend/          # Frontend deployment & Lambda
└── README.md              # This file
```

## Quick Start

1. **Copy environment template**:
```bash
cp ../template.env ../.env
# Edit .env with your values
```

2. **Create terraform.tfvars**:
```bash
cp terraform.tfvars.example terraform.tfvars
# Edit with your values
```

3. **Initialize Terraform**:
```bash
terraform init
```

4. **Plan deployment**:
```bash
terraform plan
```

5. **Deploy**:
```bash
terraform apply
```

## Module Details

### Network Module
- Creates VPC with public/private subnets across 2 AZs
- Network Load Balancer for WebSocket connections
- CloudFront distribution for global delivery
- S3 bucket for frontend hosting
- Security groups and routing

### Compute Module
- ECS Fargate cluster
- Task definition with backend container
- Service with 2 tasks for HA
- IAM roles for Bedrock and DynamoDB access

### Auth Module
- Cognito User Pool with email verification
- App Client with OAuth2 flows
- Custom domain prefix

### Frontend Module
- Lambda function to generate config.js
- S3 bucket deployment
- CloudFront cache invalidation

## Outputs

After deployment, you'll get:
- `frontend_url` - CloudFront URL for the application
- `cognito_user_pool_id` - For creating users
- `cognito_app_client_id` - For authentication
- `nlb_dns_name` - Direct NLB endpoint

## Clean Up

```bash
terraform destroy
```

## Learning Resources

Each module has its own README explaining:
- What resources it creates
- Why each resource is needed
- How they connect together
- Variables and outputs
