# Terraform Learning Guide for Nova Sonic Agent

## 🎯 Learning Path

This guide will help you understand Terraform by building the Nova Sonic infrastructure step by step.

## 📚 Prerequisites

Before starting, you should understand:
1. Basic AWS concepts (VPC, EC2, S3)
2. Docker basics
3. Command line usage

## 🏗️ Architecture Overview

```
User Browser
    ↓ HTTPS
CloudFront (CDN)
    ├── / → S3 (React Frontend)
    └── /api/* → NLB → ECS Fargate (Python Backend)
                          ↓
                    Bedrock Nova Sonic
```

## 📖 Module-by-Module Learning

### Level 1: Network Module (Start Here)
**File**: `modules/network/main.tf`

**Concepts to Learn**:
1. **VPC**: Your private network
   - CIDR blocks (IP address ranges)
   - Subnets (public vs private)
   - Route tables (traffic routing)

2. **Internet Gateway**: Connects VPC to internet
   
3. **NAT Gateway**: Allows private subnets to reach internet
   
4. **Security Groups**: Firewall rules
   - Ingress (inbound)
   - Egress (outbound)

5. **Load Balancer**: Distributes traffic
   - NLB vs ALB
   - Target groups
   - Health checks

6. **CloudFront**: CDN for global delivery
   - Origins (S3, NLB)
   - Behaviors (routing rules)
   - Caching

**Try This**:
```bash
# Deploy just the network module
cd terraform
terraform init
terraform plan -target=module.network
terraform apply -target=module.network
```

**Questions to Answer**:
- Why do we need both public and private subnets?
- What happens if NAT Gateway fails?
- Why use NLB instead of ALB?

---

### Level 2: Auth Module
**File**: `modules/auth/main.tf`

**Concepts to Learn**:
1. **Cognito User Pool**: User directory
   - Password policies
   - Email verification
   - MFA

2. **App Client**: Application configuration
   - OAuth2 flows
   - Token validity
   - Callback URLs

3. **JWT Tokens**: Authentication tokens
   - ID token (who you are)
   - Access token (what you can do)
   - Refresh token (stay logged in)

**Try This**:
```bash
# Create a test user
aws cognito-idp admin-create-user \
  --user-pool-id $(terraform output -raw cognito_user_pool_id) \
  --username testuser \
  --user-attributes Name=email,Value=test@example.com \
  --temporary-password Test123!
```

**Questions to Answer**:
- What's the difference between authentication and authorization?
- Why use Cognito instead of building your own auth?
- How does the backend validate JWT tokens?

---

### Level 3: Compute Module
**File**: `modules/compute/main.tf`

**Concepts to Learn**:
1. **ECS Cluster**: Container orchestration
   - Tasks vs Services
   - Fargate vs EC2 launch type

2. **Task Definition**: Container blueprint
   - CPU/Memory allocation
   - Environment variables
   - Port mappings

3. **IAM Roles**: Permissions
   - Task role (what container can do)
   - Execution role (what ECS can do)
   - Least privilege principle

4. **ECR**: Docker image registry
   - Image scanning
   - Lifecycle policies

**Try This**:
```bash
# View running tasks
aws ecs list-tasks --cluster $(terraform output -raw ecs_cluster_name)

# View logs
aws logs tail /ecs/sonic-agent-dev --follow

# Scale service
aws ecs update-service \
  --cluster $(terraform output -raw ecs_cluster_name) \
  --service $(terraform output -raw ecs_service_name) \
  --desired-count 3
```

**Questions to Answer**:
- Why use Fargate instead of managing EC2 instances?
- What happens when a task fails health checks?
- How does ECS pull images from ECR?

---

### Level 4: Frontend Module
**File**: `modules/frontend/main.tf`

**Concepts to Learn**:
1. **Lambda Functions**: Serverless compute
   - Event-driven execution
   - Custom resources in Terraform

2. **S3 Deployment**: Static website hosting
   - Bucket policies
   - CloudFront integration

3. **Null Resources**: Terraform tricks
   - Local-exec provisioner
   - Triggers for re-execution

**Try This**:
```bash
# Build frontend
cd ../frontend
npm install
npm run build

# Manually upload to S3
aws s3 sync dist/ s3://$(terraform output -raw frontend_bucket_name)/

# Invalidate CloudFront cache
aws cloudfront create-invalidation \
  --distribution-id $(terraform output -raw cloudfront_distribution_id) \
  --paths "/*"
```

**Questions to Answer**:
- Why use Lambda to generate config.js?
- What's the difference between S3 and CloudFront?
- How does CloudFront know when to fetch new files?

---

## 🔧 Terraform Concepts

### 1. Resources
**What**: Things Terraform creates (VPC, EC2, S3, etc.)
```hcl
resource "aws_s3_bucket" "example" {
  bucket = "my-bucket"
}
```

### 2. Data Sources
**What**: Read existing resources
```hcl
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]
}
```

### 3. Variables
**What**: Input parameters
```hcl
variable "environment" {
  type    = string
  default = "dev"
}
```

### 4. Outputs
**What**: Values to display or use elsewhere
```hcl
output "bucket_name" {
  value = aws_s3_bucket.example.bucket
}
```

### 5. Modules
**What**: Reusable Terraform code
```hcl
module "network" {
  source = "./modules/network"
  vpc_cidr = "10.0.0.0/16"
}
```

### 6. State
**What**: Terraform's memory of what it created
- Stored in `terraform.tfstate`
- Contains resource IDs, attributes
- **Never edit manually!**

---

## 🎓 Exercises

### Exercise 1: Modify Network
**Goal**: Add a third availability zone

1. Edit `terraform.tfvars`:
```hcl
availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]
```

2. Run:
```bash
terraform plan
terraform apply
```

3. Observe: Terraform creates new subnets

### Exercise 2: Change Container Size
**Goal**: Increase container resources

1. Edit `terraform.tfvars`:
```hcl
container_cpu    = 2048  # 2 vCPU
container_memory = 4096  # 4 GB
```

2. Apply and watch ECS rolling update

### Exercise 3: Add Auto-Scaling
**Goal**: Scale based on CPU usage

1. Add to `modules/compute/main.tf`:
```hcl
resource "aws_appautoscaling_target" "ecs" {
  max_capacity       = 10
  min_capacity       = 2
  resource_id        = "service/${aws_ecs_cluster.main.name}/${aws_ecs_service.main.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}
```

2. Apply and test scaling

---

## 🐛 Troubleshooting

### Common Issues

**1. "Error creating VPC: VpcLimitExceeded"**
- **Cause**: AWS account limit (default: 5 VPCs per region)
- **Fix**: Delete unused VPCs or request limit increase

**2. "Error: InvalidParameterException: Cognito domain already exists"**
- **Cause**: Domain prefix must be globally unique
- **Fix**: Change `cognito_domain_prefix` in tfvars

**3. "Error: No space left on device"**
- **Cause**: Docker images filling disk
- **Fix**: `docker system prune -a`

**4. "ECS tasks failing health checks"**
- **Cause**: Container not listening on port 80
- **Fix**: Check CloudWatch logs

### Debugging Commands

```bash
# View Terraform plan without applying
terraform plan

# Show current state
terraform show

# List all resources
terraform state list

# Show specific resource
terraform state show module.network.aws_vpc.main[0]

# Refresh state from AWS
terraform refresh

# Import existing resource
terraform import aws_s3_bucket.example my-bucket-name
```

---

## 📊 Cost Estimation

### Monthly Costs (us-east-1, 2 tasks)

| Service | Cost |
|---------|------|
| ECS Fargate (2 tasks, 1vCPU, 2GB) | ~$71 |
| NAT Gateway | ~$32 + data |
| NLB | ~$16 + data |
| CloudFront | ~$1 (low traffic) |
| S3 | <$1 |
| Cognito | Free (< 50k MAU) |
| **Total** | **~$120/month** |

### Cost Optimization
1. Use FARGATE_SPOT (70% cheaper)
2. Scale down during off-hours
3. Use VPC endpoints instead of NAT Gateway
4. Enable CloudFront caching

---

## 🚀 Next Steps

1. **Deploy the infrastructure**:
```bash
terraform init
terraform plan
terraform apply
```

2. **Create a user and test**

3. **Monitor in AWS Console**:
   - ECS → Clusters → Tasks
   - CloudWatch → Log groups
   - CloudFront → Distributions

4. **Make changes**:
   - Modify variables
   - Add auto-scaling
   - Add monitoring alarms

5. **Learn more**:
   - [Terraform Documentation](https://www.terraform.io/docs)
   - [AWS ECS Best Practices](https://docs.aws.amazon.com/AmazonECS/latest/bestpracticesguide/)
   - [Cognito Developer Guide](https://docs.aws.amazon.com/cognito/latest/developerguide/)

---

## 💡 Key Takeaways

1. **Modules = Reusability**: Break infrastructure into logical pieces
2. **State = Source of Truth**: Terraform tracks what it created
3. **Plan before Apply**: Always review changes
4. **Variables = Flexibility**: Make code reusable across environments
5. **Outputs = Integration**: Share values between modules

Happy Learning! 🎉
