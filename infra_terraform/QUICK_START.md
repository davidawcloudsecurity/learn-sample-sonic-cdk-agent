# Quick Start Guide

## 🚀 Deploy in 10 Minutes

### Prerequisites Checklist
- [ ] AWS CLI installed and configured
- [ ] Terraform >= 1.0 installed
- [ ] Docker installed
- [ ] Node.js 20+ installed
- [ ] Amazon Nova Sonic enabled in Bedrock (us-east-1)
- [ ] DynamoDB table created with sample data
- [ ] Bedrock Knowledge Base created

### Step 1: Prepare Environment (2 min)

```bash
# Navigate to terraform directory
cd sample-sonic-cdk-agent/terraform

# Copy and edit variables
cp terraform.tfvars.example terraform.tfvars
nano terraform.tfvars  # Edit with your values
```

**Required values in terraform.tfvars**:
- `cognito_domain_prefix`: Must be globally unique (e.g., `my-app-dev-12345`)
- `knowledge_base_id`: Your Bedrock KB ID
- `dynamodb_table_name`: Your DynamoDB table name

### Step 2: Build Frontend (2 min)

```bash
cd ../frontend
npm install
npm run build
cd ../terraform
```

### Step 3: Initialize Terraform (1 min)

```bash
terraform init
```

This downloads AWS provider and initializes modules.

### Step 4: Review Plan (2 min)

```bash
terraform plan
```

Review what will be created:
- VPC with subnets
- NLB and CloudFront
- ECS cluster and service
- Cognito User Pool
- S3 buckets
- IAM roles

### Step 5: Deploy (3 min)

```bash
terraform apply
```

Type `yes` when prompted.

**Note**: First deployment takes ~5-10 minutes due to:
- Docker image build and push to ECR
- ECS service startup
- CloudFront distribution creation

### Step 6: Create User (1 min)

```bash
# Get User Pool ID from outputs
USER_POOL_ID=$(terraform output -raw cognito_user_pool_id)

# Create user
aws cognito-idp admin-create-user \
  --user-pool-id $USER_POOL_ID \
  --username your-username \
  --user-attributes Name=email,Value=your-email@example.com \
  --temporary-password TempPass123! \
  --region us-east-1
```

### Step 7: Access Application (1 min)

```bash
# Get frontend URL
terraform output frontend_url
```

Open the URL in your browser and login!

---

## 📋 What Gets Created

### Network (module/network)
- ✅ VPC (10.0.0.0/16)
- ✅ 2 Public Subnets
- ✅ 2 Private Subnets
- ✅ Internet Gateway
- ✅ NAT Gateway
- ✅ Network Load Balancer
- ✅ CloudFront Distribution
- ✅ S3 Bucket (frontend)
- ✅ Security Groups

### Auth (module/auth)
- ✅ Cognito User Pool
- ✅ Cognito App Client
- ✅ Cognito Domain

### Compute (module/compute)
- ✅ ECS Cluster
- ✅ ECR Repository
- ✅ Task Definition
- ✅ ECS Service (2 tasks)
- ✅ IAM Roles
- ✅ CloudWatch Log Group

### Frontend (module/frontend)
- ✅ Lambda (config generator)
- ✅ S3 Deployment
- ✅ CloudFront Invalidation

---

## 🔍 Verify Deployment

### Check ECS Tasks
```bash
aws ecs list-tasks \
  --cluster $(terraform output -raw ecs_cluster_name) \
  --desired-status RUNNING
```

### Check Logs
```bash
aws logs tail /ecs/sonic-agent-dev --follow
```

### Check CloudFront
```bash
curl -I $(terraform output -raw frontend_url)
```

---

## 🧪 Test the Application

1. **Open frontend URL** (from terraform output)
2. **Login** with created user
3. **Change password** on first login
4. **Click "Start Session"**
5. **Speak** into microphone
6. **Hear** Nova Sonic response

---

## 🛠️ Common Commands

### View Outputs
```bash
terraform output
```

### Update Infrastructure
```bash
# After changing variables or code
terraform plan
terraform apply
```

### Scale ECS Service
```bash
aws ecs update-service \
  --cluster $(terraform output -raw ecs_cluster_name) \
  --service $(terraform output -raw ecs_service_name) \
  --desired-count 4
```

### Redeploy Frontend
```bash
cd ../frontend
npm run build
cd ../terraform
terraform apply -target=module.frontend
```

### View State
```bash
terraform show
terraform state list
```

---

## 🧹 Clean Up

### Destroy Everything
```bash
terraform destroy
```

Type `yes` when prompted.

**Note**: This will delete:
- All infrastructure
- S3 buckets (and contents)
- CloudWatch logs
- ECR images

**Preserved** (manual deletion required):
- DynamoDB table
- Bedrock Knowledge Base

---

## ❌ Troubleshooting

### Issue: "Cognito domain already exists"
**Solution**: Change `cognito_domain_prefix` in terraform.tfvars to something unique

### Issue: "No space left on device"
**Solution**: 
```bash
docker system prune -a
```

### Issue: ECS tasks not starting
**Solution**: Check logs
```bash
aws logs tail /ecs/sonic-agent-dev --follow
```

### Issue: Frontend not loading
**Solution**: Check CloudFront distribution status
```bash
aws cloudfront get-distribution \
  --id $(terraform output -raw cloudfront_distribution_id) \
  --query 'Distribution.Status'
```

### Issue: WebSocket connection fails
**Solution**: 
1. Check ECS tasks are running
2. Check NLB target health
3. Verify Cognito token is valid

---

## 📊 Monitoring

### CloudWatch Dashboards
```bash
# View ECS metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/ECS \
  --metric-name CPUUtilization \
  --dimensions Name=ServiceName,Value=$(terraform output -raw ecs_service_name) \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Average
```

### Cost Tracking
```bash
# View current month costs
aws ce get-cost-and-usage \
  --time-period Start=$(date +%Y-%m-01),End=$(date +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --group-by Type=SERVICE
```

---

## 🎓 Next Steps

1. **Read LEARNING_GUIDE.md** for deep dive into each module
2. **Customize** system prompts and tools
3. **Add monitoring** alarms
4. **Enable auto-scaling**
5. **Set up CI/CD** pipeline

---

## 📚 Resources

- [Terraform AWS Provider Docs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [AWS ECS Documentation](https://docs.aws.amazon.com/ecs/)
- [Amazon Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Module READMEs](./modules/) - Detailed explanations

---

## 💬 Need Help?

Check the module-specific READMEs:
- `modules/network/README.md` - VPC, NLB, CloudFront
- `modules/auth/README.md` - Cognito authentication
- `modules/compute/README.md` - ECS Fargate
- `modules/frontend/README.md` - S3 and Lambda

Happy deploying! 🎉
