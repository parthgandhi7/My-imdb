# CI/CD Plan for Deploying My-imdb to Vercel

This document proposes a practical CI/CD strategy for deploying **My-imdb** to Vercel with clear promotion rules, quality gates, and rollback steps.

## 1) Goals

- Deploy every change safely and quickly.
- Gate production deployments behind automated checks.
- Keep preview environments easy to review.
- Ensure secrets and environment variables are managed safely.

## 2) Recommended Environment Model

Use Vercel's three environment types:

- **Development**: local and ad-hoc development (`vercel env pull`).
- **Preview**: every pull request gets a unique preview URL.
- **Production**: deploy only from the `main` branch.

### Git Branching

- `main`: production-ready branch.
- Feature branches: PRs into `main`.

## 3) Pipeline Overview

### Trigger points

1. **Pull Request opened/synchronized**
   - Run CI checks (lint, test, build).
   - Create/update Vercel Preview deployment.
2. **Merge to `main`**
   - Run CI checks again.
   - Deploy to Vercel Production.

### Quality Gates (minimum)

Before allowing merge:
- Lint passes.
- Tests pass.
- Build succeeds.
- (Optional) Basic security scan passes.

## 4) Vercel Project Setup (One-time)

1. Import GitHub repository into Vercel.
2. Confirm framework preset and build output.
3. Configure environment variables:
   - Add values for Development, Preview, and Production scopes.
4. Configure branch settings:
   - Production branch = `main`.
5. Enable Vercel protection rules if desired (password or trusted users for previews).

## 5) GitHub Setup

## Required repository secrets

Add these GitHub Actions secrets:

- `VERCEL_TOKEN`: personal/team token from Vercel.
- `VERCEL_ORG_ID`: Vercel team/org ID.
- `VERCEL_PROJECT_ID`: target Vercel project ID.

## Branch protections for `main`

Enable:
- Require pull request before merge.
- Require status checks to pass.
- Require up-to-date branch before merging.
- Restrict direct pushes (recommended).

## 6) Suggested GitHub Actions Workflow

Create `.github/workflows/vercel.yml` with two jobs:

1. **ci** job (PR + push):
   - Checkout code.
   - Install dependencies.
   - Run lint/test/build commands.
2. **deploy-preview** (on PR):
   - `vercel pull --environment=preview`
   - `vercel build`
   - `vercel deploy --prebuilt`
3. **deploy-production** (on push to `main`):
   - `vercel pull --environment=production`
   - `vercel build --prod`
   - `vercel deploy --prebuilt --prod`

> If the project grows, split CI and deploy into separate workflows for cleaner ownership.

## 7) Operational Standards

## Observability

- Use Vercel Analytics and function logs.
- Track deployment status from both Vercel and GitHub Actions.

## Rollback

- Roll back instantly by promoting a previous successful deployment in Vercel.
- Keep release notes in PR descriptions for traceability.

## Incident response

- If production fails post-deploy:
  1. Trigger rollback immediately.
  2. Open hotfix PR.
  3. Validate in preview.
  4. Merge to `main` and redeploy.

## 8) Security Practices

- Never store secrets in repository files.
- Use least-privilege Vercel token.
- Rotate tokens periodically.
- Run dependency checks (e.g., `npm audit` or SCA tool) on schedule.

## 9) Step-by-Step Implementation Plan

1. Connect repo to Vercel.
2. Add required Vercel environment variables.
3. Add GitHub secrets (`VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`).
4. Add GitHub Action workflow for CI + deploy.
5. Enable branch protections on `main`.
6. Open a test PR and verify preview deployment.
7. Merge PR and verify production deployment.
8. Document rollback runbook in repository.

## 10) Definition of Done

This CI/CD setup is considered complete when:

- Every PR gets a successful preview URL.
- `main` merges automatically deploy to production.
- Production deploys are blocked if CI fails.
- Rollback is tested at least once.
- Secrets are scoped to correct environments.
