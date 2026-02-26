# Two-Factor Authentication Playbook

Use this playbook for 2FA rollout using TOTP and/or OTP flows.

## 1) Base Setup

- Enable 2FA plugin and client plugin.
- Run schema migration after plugin changes.
- Ensure UX includes explicit verification and fallback recovery path.

## 2) TOTP Flow

- Enable with issuer/app name.
- Generate QR from TOTP URI.
- Confirm verification path before marking fully enabled.

## 3) OTP Flow

- Configure secure OTP delivery channel.
- Tune validity window, attempt limits, and storage strategy.

## 4) Backup Codes and Recovery

- Display backup codes once at enrollment.
- Support regeneration with clear invalidation semantics.
- Test backup-code sign-in and revocation behavior.

## 5) Trusted Device and Risk Controls

- Enable trust-device only when policy allows.
- Add rate limits around verification endpoints.
- Require credential confirmation for sensitive 2FA state changes.

## Upstream References

- `../upstream/better-auth/llms.txt/docs/plugins/2fa.md`
- `../upstream/better-auth/llms.txt/docs/concepts/session-management.md`
- `../upstream/better-auth/llms.txt/docs/reference/options.md`
