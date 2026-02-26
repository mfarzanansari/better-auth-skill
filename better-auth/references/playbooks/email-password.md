# Email and Password Playbook

Use this playbook for email/password authentication, verification, reset, and password policy hardening.

## 1) Required Components

- `emailAndPassword.enabled`
- Verification flow (`emailVerification.sendVerificationEmail`) when verification is required
- Reset flow (`sendResetPassword`) for account recovery

## 2) Recommended Policy

- Require email verification for production-grade apps.
- Use absolute callback URLs for multi-origin deployments.
- Configure password min/max length appropriate to threat model.
- Revoke active sessions on password reset where security-sensitive.

## 3) Reset and Recovery

- Ensure reset token expiry aligns with risk profile.
- Ensure single-use token behavior is preserved.
- Use neutral user-facing responses to reduce account enumeration risk.

## 4) Hashing and Algorithm Strategy

- Default hashing can be retained for most apps.
- If custom algorithm is used, plan migration compatibility for existing hashes.

## 5) Validation Checklist

- Verification flow works end-to-end.
- Reset flow works end-to-end.
- Invalid/expired token paths fail safely.
- Session revocation behavior matches policy.

## Upstream References

- `../upstream/better-auth/llms.txt/docs/authentication/email-password.md`
- `../upstream/better-auth/llms.txt/docs/concepts/email.md`
- `../upstream/better-auth/llms.txt/docs/reference/options.md`
- `../upstream/better-auth/llms.txt/docs/plugins/email-otp.md`
- `../upstream/better-auth/llms.txt/docs/plugins/magic-link.md`
