---
name: better-auth
description: Framework-agnostic Better Auth implementation and troubleshooting skill for TypeScript applications. Use when setting up Better Auth, migrating from Auth.js/Auth0/Clerk/Supabase/WorkOS, configuring adapters/providers/plugins, hardening security settings, or diagnosing Better Auth runtime/auth/session errors.
---

# Better Auth

## Overview

Use this skill to deliver production-grade Better Auth setup, migration, and debugging with explicit workflow gates.

Keep this file procedural. Load details from `references/playbooks/` first, then exact upstream docs in `references/upstream/`.

## Required Workflow

1. Scan project context before implementation.
2. Capture requirements and decide path.
3. Route to the smallest playbook/reference set.
4. Apply minimum changes.
5. Validate auth flows and safety checks.

Do not skip project scan or requirement intake.

## Phase 1: Project Scan and Requirement Intake

Before writing code, confirm:

- Framework/runtime: Next.js, SvelteKit, Nuxt, Express, Hono, etc.
- Database and adapter stack: Prisma, Drizzle, direct driver, MongoDB.
- Existing auth system and migration status.
- Required sign-in methods (email/password, social OAuth, magic link, passkey, phone).
- Required plugins (2FA, organization, bearer/API key, SSO/OIDC/OAuth provider, etc.).
- Email delivery strategy for verification/reset/invitations.
- Security constraints (trusted origins, session policy, CSRF, rate limits).

If any of these are unknown, ask before implementation.

## Phase 2: Route to the Right Branch

### Branch A: Core Setup / Migration

Use when creating first Better Auth integration or migrating from another provider.

Load in order:

1. `references/playbooks/core-setup-migration.md`
2. Relevant migration guide in `references/upstream/better-auth/llms.txt/docs/guides/`
3. Framework integration doc in `references/upstream/better-auth/llms.txt/docs/integrations/`
4. Adapter doc in `references/upstream/better-auth/llms.txt/docs/adapters/`

### Branch B: Security Hardening

Use when auditing security or fixing trust/session/rate-limit weaknesses.

Load in order:

1. `references/playbooks/security-baseline.md`
2. `references/upstream/better-auth/llms.txt/docs/reference/security.md`
3. `references/upstream/better-auth/llms.txt/docs/reference/options.md`

### Branch C: Email/Password Flows

Use for signup/signin/reset/verification/password policy behavior.

Load:

1. `references/playbooks/email-password.md`
2. `references/upstream/better-auth/llms.txt/docs/authentication/email-password.md`
3. Relevant plugin docs (`email-otp`, `magic-link`, etc.) if used.

### Branch D: Organization and Multi-Tenant Flows

Use for org lifecycle, membership, invitations, role/permission patterns.

Load:

1. `references/playbooks/organization.md`
2. `references/upstream/better-auth/llms.txt/docs/plugins/organization.md`

### Branch E: Two-Factor Flows

Use for TOTP/OTP, backup codes, trusted devices, and 2FA onboarding.

Load:

1. `references/playbooks/two-factor.md`
2. `references/upstream/better-auth/llms.txt/docs/plugins/2fa.md`

### Branch F: Providers and Error Diagnosis

Use for OAuth/provider setup and explicit error troubleshooting.

Load:

1. `references/playbooks/providers-and-errors.md`
2. `references/error-map.md`
3. Exact error docs in `references/upstream/better-auth/llms.txt/docs/reference/errors/`

## Guardrails

- Re-run Better Auth CLI schema generation/migrations after adding or changing plugins.
- Verify env vars and callback/trusted-origin config before concluding root cause.
- Keep fixes scoped to the failing flow; avoid unrelated refactors.
- Use model names (adapter/ORM semantics), not raw table names, when required by adapter config.
- Prefer dedicated plugin import paths over broad plugin imports.

## Validation Checklist

For any meaningful auth change:

1. Positive path works (signup/signin/session/use case success).
2. Negative path is handled (invalid credentials/token/provider mismatch).
3. Session behavior is correct (creation, refresh, revocation/log out).
4. Security policy is enforced (origins/rate limits/verification where configured).
5. Schema state is synchronized after plugin changes.

## Refresh Upstream Docs

```bash
python3 better-auth/scripts/fetch_better_auth_llms.py
```

Useful modes:

```bash
python3 better-auth/scripts/fetch_better_auth_llms.py --dry-run
python3 better-auth/scripts/fetch_better_auth_llms.py --prune
```

## Resource Map

- Playbook index: `references/index.md`
- Error triage map: `references/error-map.md`
- Merged playbooks: `references/playbooks/`
- Upstream corpus: `references/upstream/better-auth/`
- Refresh script: `scripts/fetch_better_auth_llms.py`
