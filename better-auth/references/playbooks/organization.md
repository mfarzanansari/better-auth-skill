# Organization Playbook

Use this playbook for multi-tenant organization setup, membership, invitations, and role governance.

## 1) Base Plugin Setup

- Enable organization plugin with clear limits/policies.
- Add matching client-side plugin.
- Run schema migration after plugin introduction.
- Validate organization/member/invitation tables after migration.

## 2) Organization Lifecycle

- Create org with explicit owner semantics.
- Set active organization before org-scoped operations.
- Define org creation limits and policy hooks.
- Use server-side creation APIs when creating orgs on behalf of users.

## 3) Membership and Roles

- Define role model and permission boundaries.
- Validate owner-protection constraints (for example preventing orphaned orgs).
- Use invitation flow for standard member onboarding.
- For advanced RBAC, route to dynamic access control addon patterns.

## 4) Invitation Security

- Configure invitation expiry and re-invite behavior.
- Ensure callback URLs are trusted-origin safe.
- Handle accept/reject/cancel paths explicitly.

## 5) Teams, Hooks, and Schema Extensions

- Use teams only when org membership semantics are stable.
- Add lifecycle hooks for provisioning/auditing (organization/member/invitation events).
- Customize schema fields only with explicit migration and backward-compatibility plan.

## 6) Validation Checklist

- Active org context is correctly enforced.
- Member role updates are permission-checked.
- Invitation lifecycle behaves as configured.
- Last-owner and deletion edge cases are guarded.
- Team membership operations enforce org membership prerequisites.

## Upstream References

- `../upstream/better-auth/llms.txt/docs/plugins/organization.md`
- `../upstream/better-auth/llms.txt/docs/concepts/users-accounts.md`
- `../upstream/better-auth/llms.txt/docs/reference/options.md`
