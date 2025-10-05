# CodeBuild ARM64 Image Builder

Scripts to build ARM64 AgentCore images using AWS CodeBuild to resolve `create_react_agent` import issues.

## Problem
Local ARM64 cross-compilation fails with dependency conflicts. CodeBuild ARM64 environment provides native ARM64 build capability.

## Setup Steps

### 1. Create S3 Bucket
```bash
./setup-s3-bucket.sh
```

### 2. Create IAM Role
```bash
./create-iam-role.sh
```

### 3. Upload Agent Sources
```bash
./upload-codebuild-sources.sh
```

### 4. Create CodeBuild Projects
```bash
./create-codebuild-projects.sh
```

### 5. Start Individual Builds
```bash
aws codebuild start-build --project-name agentcore-purchase-builder --region us-east-1
aws codebuild start-build --project-name agentcore-cement-builder --region us-east-1
aws codebuild start-build --project-name agentcore-steel-builder --region us-east-1
```

## Files

- `setup-s3-bucket.sh` - Creates S3 bucket for source storage
- `create-iam-role.sh` - Creates IAM role with ECR/S3 permissions
- `upload-codebuild-sources.sh` - Uploads individual agent sources to S3
- `create-codebuild-projects.sh` - Creates separate CodeBuild projects for each agent
- `cleanup.sh` - Removes all CodeBuild resources

## Agent Structure

Each agent has its own buildspec.yml:
- `agentcore-agents/purchase_agent/buildspec.yml`
- `agentcore-agents/cement_agent/buildspec.yml`
- `agentcore-agents/steel_agent/buildspec.yml`

## Environment

- **Compute**: ARM64 native (BUILD_GENERAL1_LARGE)
- **Image**: aws/codebuild/amazonlinux2-aarch64-standard:3.0
- **Source**: S3 bucket with individual agent zips
- **Output**: ARM64 images pushed to ECR

## Benefits

- Native ARM64 compilation (no emulation)
- Resolves dependency conflicts
- Separate builds for each agent
- Automated ECR push
- Scalable build environment