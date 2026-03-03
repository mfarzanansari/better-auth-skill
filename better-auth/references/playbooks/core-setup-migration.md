# Core Setup and Migration Playbook

Use this playbook for first-time Better Auth setup or migration from another auth stack.

## 1) Intake Matrix

Capture and lock these decisions before coding:

- Framework: Next.js App/Pages Router, SvelteKit, Nuxt, React Router v7, Express, Hono, Electron, etc.
- Database model: direct DB driver vs Prisma/Drizzle/Mongo adapter.
- Auth methods: email/password, social OAuth, magic link, passkey, phone.
- Plugin set: 2FA, org, admin, bearer/api-key, SSO, provider features.
- Managed services scope: Better Auth Infrastructure (`@better-auth/infra`) dashboard/sentinel/email/sms.
- Migration source: Auth.js, Auth0, Clerk, Supabase Auth, WorkOS, custom.
- Package manager and `auth.ts` location (default lookup paths or custom `--config`).

## 2) Project Scan Before Changes

- Detect framework config files and route conventions.
- Detect adapter/ORM files (`prisma/schema.prisma`, drizzle config, DB driver deps).
- Detect existing auth libraries and migration surface.
- Detect lockfile to choose install/migration command style.

## 3) Baseline Setup Sequence

1. Install Better Auth and required plugin packages.
2. Create server auth config (`auth.ts`) with adapter + selected methods.
3. Create client auth entry (`auth-client.ts`) for framework.
4. Wire route handler/integration for framework.
5. Configure env vars (`BETTER_AUTH_SECRET`, `BETTER_AUTH_URL`, provider secrets).
6. If using infrastructure services, configure `BETTER_AUTH_API_KEY` and infra plugin options.
7. Run schema command:
- Built-in adapter: `migrate`
- Prisma/Drizzle: `generate` + ORM migration command
8. Validate `/api/auth/ok` endpoint health check.
9. Validate signup/signin/session/revoke flow.

## 4) Migration Sequence

1. Inventory current auth behavior and required backward compatibility.
2. Map old concepts to Better Auth (session, account linking, verification, reset).
3. Migrate schema/data path in controlled steps.
4. Move routes/handlers and client auth calls.
5. Migrate feature plugins incrementally.
6. Remove legacy auth once parity checks pass.

## 5) Adapter and Integration Routing

- Adapter docs: `../upstream/better-auth/llms.txt/docs/adapters/`
- Integration docs: `../upstream/better-auth/llms.txt/docs/integrations/`
- Migration guides: `../upstream/better-auth/llms.txt/docs/guides/`
- Infrastructure docs: `../upstream/better-auth/llms.txt/docs/infrastructure/`

## 6) Guardrails

- Re-run schema commands whenever plugin set changes.
- Confirm adapter model naming semantics before mapping tables/fields.
- Use absolute callback URLs when frontend/backend origins differ.
- Verify `trustedOrigins` and redirect handling during migration cutover.
- Prefer plugin-specific import paths for better tree-shaking and clearer ownership.
