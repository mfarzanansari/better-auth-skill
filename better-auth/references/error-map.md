# Better Auth Error Map

Use this map to route from runtime errors to the exact upstream explanation and fix path.

## Triage Workflow

1. Capture exact error token and failing endpoint.
2. Route to exact error doc below.
3. Validate related configuration family (provider, callback/origin, signup policy, account linking).
4. Implement smallest fix.
5. Re-test failing flow and one adjacent flow.

## Token -> Upstream Error Doc

- `account_already_linked_to_different_user` -> `upstream/better-auth/llms.txt/docs/reference/errors/account_already_linked_to_different_user.md`
- `email_doesn't_match` -> `upstream/better-auth/llms.txt/docs/reference/errors/email_doesn't_match.md`
- `email_not_found` -> `upstream/better-auth/llms.txt/docs/reference/errors/email_not_found.md`
- `invalid_callback_request` -> `upstream/better-auth/llms.txt/docs/reference/errors/invalid_callback_request.md`
- `no_callback_url` -> `upstream/better-auth/llms.txt/docs/reference/errors/no_callback_url.md`
- `no_code` -> `upstream/better-auth/llms.txt/docs/reference/errors/no_code.md`
- `oauth_provider_not_found` -> `upstream/better-auth/llms.txt/docs/reference/errors/oauth_provider_not_found.md`
- `signup_disabled` -> `upstream/better-auth/llms.txt/docs/reference/errors/signup_disabled.md`
- `state_mismatch` -> `upstream/better-auth/llms.txt/docs/reference/errors/state_mismatch.md`
- `state_not_found` -> `upstream/better-auth/llms.txt/docs/reference/errors/state_not_found.md`
- `unable_to_get_user_info` -> `upstream/better-auth/llms.txt/docs/reference/errors/unable_to_get_user_info.md`
- `unable_to_link_account` -> `upstream/better-auth/llms.txt/docs/reference/errors/unable_to_link_account.md`
- `unknown` -> `upstream/better-auth/llms.txt/docs/reference/errors/unknown.md`

## Related Root-Cause Families

### Provider and OAuth wiring

Use when seeing provider lookup/state/code/callback failures:

- `upstream/better-auth/llms.txt/docs/authentication/`
- `upstream/better-auth/llms.txt/docs/plugins/generic-oauth.md`
- `upstream/better-auth/llms.txt/docs/plugins/oauth-provider.md`
- `upstream/better-auth/llms.txt/docs/plugins/oidc-provider.md`

### Origin and callback trust

Use when callback/origin validation fails:

- `upstream/better-auth/llms.txt/docs/reference/options.md`
- `upstream/better-auth/llms.txt/docs/reference/security.md`

### Signup and account linking policy

Use when signup or linking behavior is blocked:

- `upstream/better-auth/llms.txt/docs/concepts/users-accounts.md`
- `upstream/better-auth/llms.txt/docs/reference/options.md`

## Fallback

If token is not listed:

1. Check `upstream/better-auth/llms.txt/docs/reference/errors.md`.
2. Search category docs tied to the failing endpoint (provider/plugin/integration).
3. Verify env vars, callback URLs, trusted origins, and plugin-specific schema state.
