# better-auth-skill

Public distribution repository for the `better-auth` agent skill.

This repo ships one enhanced Better Auth skill that combines:

- Core setup and migration workflows
- Security hardening workflows
- Email/password best-practice workflows
- Organization and multi-tenant workflows
- 2FA workflows
- Provider + error diagnosis workflows

It also bundles Better Auth upstream docs and a refresh script for deterministic updates.

## Install

Install this specific skill:

```bash
npx skills add https://github.com/mfarzanansari/better-auth-skill --skill better-auth
```

List skills in this repository:

```bash
npx skills add https://github.com/mfarzanansari/better-auth-skill --list
```

Install from shorthand (if repository is public and resolvable):

```bash
npx skills add mfarzanansari/better-auth-skill --skill better-auth
```

## What This Skill Does

The `better-auth` skill helps agents:

- Set up Better Auth in framework-specific projects
- Migrate from Auth.js/Auth0/Clerk/Supabase/WorkOS
- Configure adapters/providers/plugins safely
- Troubleshoot Better Auth errors and callback/origin issues
- Apply security baseline checks for sessions, CSRF, rate limits, and secrets

## Skill Layout

- `better-auth/SKILL.md` - workflow orchestrator
- `better-auth/agents/openai.yaml` - UI metadata
- `better-auth/scripts/fetch_better_auth_llms.py` - upstream docs refresh script
- `better-auth/references/playbooks/` - curated merged playbooks
- `better-auth/references/upstream/better-auth/` - bundled Better Auth upstream docs corpus

## Refresh Upstream Docs

Dry run:

```bash
python3 better-auth/scripts/fetch_better_auth_llms.py --dry-run
```

Full refresh:

```bash
python3 better-auth/scripts/fetch_better_auth_llms.py
```

Refresh and prune stale files:

```bash
python3 better-auth/scripts/fetch_better_auth_llms.py --prune
```

## Compatibility

This repository is compatible with the `skills` CLI ecosystem and agent targets such as Codex, Cursor, Claude Code, and others supported by the CLI.

Reference CLI:

- `npx skills add ...`
- `npx skills list`
- `npx skills check`

## Troubleshooting

### `--list` shows no skills

- Verify repository URL is correct and public.
- Confirm `better-auth/SKILL.md` exists in the default branch.
- Re-run with full URL instead of shorthand.

### Install succeeds but skill is not used

- Confirm skill name in frontmatter is `better-auth`.
- Confirm description includes trigger contexts (setup/migration/provider/plugin/security/debugging).
- Ensure your agent installation path is in the current project/global scope expected by the CLI.

### Refresh script failures

- Re-run with `--dry-run` to isolate connectivity/path issues.
- Confirm access to `https://www.better-auth.com/llms.txt`.

## Publication Notes

### skills.sh

Discovery is telemetry-driven via `skills` CLI installs. After users install this repo/skill, the source should appear on the leaderboard over time.

Expected source page pattern:

- `https://skills.sh/mfarzanansari`

### skillsmp.com Manual Checklist

Because automated workflow details are not verifiable from docs in this environment, use this manual checklist:

1. Submit GitHub repo URL: `https://github.com/mfarzanansari/better-auth-skill`
2. Submit canonical install command:
   - `npx skills add https://github.com/mfarzanansari/better-auth-skill --skill better-auth`
3. Submit skill metadata:
   - Name: `better-auth`
   - Description: from `better-auth/SKILL.md` frontmatter
4. Submit docs URL:
   - `https://github.com/mfarzanansari/better-auth-skill#readme`
5. Validate rendered page and install snippet after indexing.

## License

MIT
