# Organization Playbook

Use this playbook for multi-tenant organization setup, membership, invitations, and role governance.

## 1) Base Plugin Setup

- Enable organization plugin with clear limits/policies.
- Add matching client-side plugin.
- Run schema migration after plugin introduction.

## 2) Organization Lifecycle

- Create org with explicit owner semantics.
- Set active organization before org-scoped operations.
- Define org creation limits and policy hooks.

## 3) Membership and Roles

- Define role model and permission boundaries.
- Validate owner-protection constraints (for example preventing orphaned orgs).
- Use invitation flow for standard member onboarding.

## 4) Invitation Security

- Configure invitation expiry and re-invite behavior.
- Ensure callback URLs are trusted-origin safe.
- Handle accept/reject/cancel paths explicitly.

## 5) Validation Checklist

- Active org context is correctly enforced.
- Member role updates are permission-checked.
- Invitation lifecycle behaves as configured.
- Last-owner and deletion edge cases are guarded.

## Upstream References

- `../upstream/better-auth/llms.txt/docs/plugins/organization.md`
- `../upstream/better-auth/llms.txt/docs/concepts/users-accounts.md`
- `../upstream/better-auth/llms.txt/docs/reference/options.md`
