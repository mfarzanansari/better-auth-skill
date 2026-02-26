# Providers and Errors Playbook

Use this playbook for OAuth/provider configuration and error-driven debugging.

## 1) Provider Setup Flow

1. Identify provider and auth method target.
2. Confirm required provider credentials and callback URL format.
3. Confirm Better Auth provider config shape.
4. Verify route/integration and environment loading.
5. Test successful callback and denied/error callback paths.

## 2) Provider Routing

- Social/auth provider docs:
- `../upstream/better-auth/llms.txt/docs/authentication/`
- Generic provider extensions:
- `../upstream/better-auth/llms.txt/docs/plugins/generic-oauth.md`
- Provider stack extensions:
- `../upstream/better-auth/llms.txt/docs/plugins/oauth-provider.md`
- `../upstream/better-auth/llms.txt/docs/plugins/oidc-provider.md`

## 3) Error-First Debugging Flow

1. Capture exact Better Auth error token and failing endpoint.
2. Route through `../error-map.md`.
3. Open exact upstream error doc under `../upstream/better-auth/llms.txt/docs/reference/errors/`.
4. Validate config/env/origin/callback assumptions.
5. Re-test failing path + nearby related paths.

## 4) Common Root-Cause Families

- Provider not found or misnamed provider block
- Callback/origin mismatch
- Missing code/state in OAuth callback
- Email/account-linking conflicts
- Signup policy restrictions

## Upstream References

- `../upstream/better-auth/llms.txt/docs/reference/errors.md`
- `../upstream/better-auth/llms.txt/docs/reference/errors/`
- `../upstream/better-auth/llms.txt/docs/authentication/`
- `../upstream/better-auth/llms.txt/docs/reference/options.md`
