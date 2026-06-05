# CICD Demo — Infrastructure as Code Pipeline

A production-ready Terraform + GitHub Actions CI/CD pipeline for deploying AWS infrastructure with automated linting, planning, and applying.

## Overview

This repository demonstrates best practices for managing infrastructure through code:

- **Infrastructure Modules**: Reusable Terraform modules for consistent deployments
- **Automated CI/CD**: GitHub Actions validates, plans, and applies Terraform changes
- **State Management**: Git-tracked Terraform state for reproducibility
- **PR Reviews**: Plan output posted to PRs for visibility before apply

## Project Structure

```
.
├── main.tf                    # Root module entry point
├── variables.tf               # Input variables (region, instance count, etc.)
├── outputs.tf                 # Root module outputs
├── modules/
│   └── staging/               # Staging environment module
│       ├── main.tf            # EC2 + Security Group resources
│       ├── variables.tf        # Module inputs
│       └── outputs.tf          # Module outputs
└── .github/workflows/
    ├── lint.yml               # Fmt, validate, tflint checks
    ├── plan.yml               # Runs terraform plan on PR
    └── apply.yml              # Runs terraform apply on main
```

## Features

### Staging Environment Module

Deploys a configurable AWS staging environment:
- **EC2 Instances**: Configurable count (default: 1 × t2.micro)
- **Security Group**: Allows HTTP (80), HTTPS (443), SSH (22)
- **Auto-tagged**: All resources tagged with environment and project metadata

### CI/CD Workflow

| Job | Trigger | Actions |
|-----|---------|---------|
| **Lint** | PR opened | `terraform fmt`, `validate`, `tflint` |
| **Plan** | PR updated | Posts `terraform plan` output to PR for review |
| **Apply** | PR merged to main | Executes `terraform apply`, commits state |

## Quick Start

### Prerequisites

- Terraform >= 1.0
- AWS credentials (export `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY`)
- GitHub CLI (`gh`) for PR management

### Local Development

```bash
# Initialize Terraform
terraform init

# Validate configuration
terraform validate

# Preview changes
terraform plan -out=tfplan

# Apply changes (if safe)
terraform apply tfplan
```

### Using the CI/CD Pipeline

1. **Create a feature branch**:
   ```bash
   git checkout -b feat/add-staging-env
   ```

2. **Make infrastructure changes** (edit `main.tf`, `variables.tf`, or modules)

3. **Commit and push**:
   ```bash
   git add .
   git commit -m "feat: add staging environment module"
   git push origin feat/add-staging-env
   ```

4. **Create a PR**:
   ```bash
   gh pr create --title "feat: add staging env" \
     --body "Adds staging environment using modular Terraform"
   ```

5. **CI runs automatically**:
   - Lint job validates code formatting and syntax
   - Plan job posts `terraform plan` to PR
   - Reviewer inspects plan diff in PR comments

6. **Merge and deploy**:
   ```bash
   gh pr merge --squash
   ```
   - Apply job runs automatically
   - `terraform apply` executes the plan
   - State file committed back to repo

## Variables

### Root Module (`variables.tf`)

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `aws_region` | string | `us-east-1` | AWS region for resources |
| `staging_instance_count` | number | `1` | Number of EC2 instances in staging |

### Example `terraform.tfvars`

```hcl
aws_region              = "us-west-2"
staging_instance_count  = 2
```

## Outputs

| Output | Description |
|--------|-------------|
| `staging_instance_ids` | EC2 instance IDs |
| `staging_instance_ips` | Public IPs of instances |
| `staging_security_group_id` | Security group ID |

Access via:
```bash
terraform output staging_instance_ips
```

## Troubleshooting

### CI Failures

#### Format Error
```
Error: Files not formatted
```
**Fix**: Run locally and commit:
```bash
terraform fmt -recursive
git add . && git commit -m "fix: apply terraform fmt"
```

#### Validation Error
```
Error: Reference to undeclared resource
```
**Fix**: Check variable/resource references:
```bash
terraform validate
```

#### State Conflicts
```
Error: state is locked / state out of sync
```
**Fix**: Sync with main and replan:
```bash
git pull origin main
git rebase origin/main
terraform plan
```

### View CI Logs

```bash
# List recent runs
gh run list

# View summary
gh run view <run-id>

# Full log output
gh run view <run-id> --log

# Watch live
gh run watch
```

## State Management

- Terraform state is stored in the repo (`.gitignore` prevents accidental deletion)
- State is committed after successful `terraform apply` via the **Apply** job
- For production, migrate to remote state (Terraform Cloud, S3 backend, etc.)

## Security Notes

- Credentials are NOT stored in the repo
- Use GitHub Secrets for sensitive variables (e.g., `AWS_ACCESS_KEY_ID`)
- Apply job requires branch protection + PR reviews (recommended)

## Contributing

1. Create a feature branch
2. Validate locally: `terraform validate && terraform plan`
3. Push and open a PR
4. Wait for CI checks and plan review
5. Request approval and merge

## License

See [LICENSE.txt](LICENSE.txt)

---

**Next Steps**:
- [ ] Configure remote state backend (AWS S3 + DynamoDB)
- [ ] Add production environment module
- [ ] Set up branch protection rules on `main`
- [ ] Integrate Sentinel policies for cost control
