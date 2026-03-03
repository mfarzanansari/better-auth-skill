# Security Baseline Playbook

Use this playbook for Better Auth security audits and hardening.

## 1) Secret and Configuration Safety

- Ensure `BETTER_AUTH_SECRET` is strong and managed in env/secrets manager.
- Confirm fallback secret/env behavior (`options.secret`, `BETTER_AUTH_SECRET`, `AUTH_SECRET`) is intentional.
- Avoid placeholder/default secrets in production.
- Keep auth base URL and trusted origins aligned with deployed domains.

## 2) Rate Limiting

- Enable and tune rate limit policy for auth-sensitive endpoints.
- Prefer durable storage (`database` or `secondary-storage`) over process memory in production.
- Apply stricter custom rules to sign-in/sign-up/password endpoints.

## 3) CSRF and Origin Controls

- Keep CSRF checks enabled unless there is a justified alternative control.
- Validate trusted origins for callback and redirect parameters.
- Confirm cross-origin request behavior for frontend/backend split deployments.
- Use dynamic trusted-origin resolution only with strict tenant/source validation.

## 4) Session Security

- Set explicit session expiry/update policy.
- Use appropriate cookie cache strategy (`compact`, `jwt`, or `jwe`) for risk profile.
- Require fresh sessions for sensitive operations where needed.
- Revoke sessions on sensitive state changes (for example after password reset).

## 5) OAuth and Provider Security

- Validate callback URL registration and provider secret handling.
- Enforce strict origin/callback configuration.
- Verify account-linking behavior for multi-provider scenarios.
- Verify state handling and proxy header/path preservation for callback flows.

## 6) Managed Security and Monitoring (Optional)

- If using Better Auth Infrastructure, validate `BETTER_AUTH_API_KEY` and plugin wiring.
- For abuse protection, review Sentinel defaults and high-risk endpoint policies.
- For auditing, verify security events are emitted and queryable through audit logs.

## 7) IP and Proxy Controls

- Validate IP tracking behavior for rate limiting and anomaly detection.
- Configure trusted proxy headers only when the reverse proxy is controlled.
- Tune IPv6 subnet grouping when abuse prevention depends on source aggregation.

## 8) Security Validation Checklist

- Failed auth attempts are rate-limited.
- Callback/open redirect abuse is blocked.
- Session invalidation works on logout/reset-sensitive flows.
- Security headers/proxy settings do not break origin detection.
- Audit trail contains key auth and security events.

## Upstream References

- `../upstream/better-auth/llms.txt/docs/reference/security.md`
- `../upstream/better-auth/llms.txt/docs/reference/options.md`
- `../upstream/better-auth/llms.txt/docs/concepts/session-management.md`
- `../upstream/better-auth/llms.txt/docs/concepts/rate-limit.md`
- `../upstream/better-auth/llms.txt/docs/concepts/oauth.md`
- `../upstream/better-auth/llms.txt/docs/infrastructure/plugins/sentinel.md`
- `../upstream/better-auth/llms.txt/docs/infrastructure/plugins/audit-logs.md`
