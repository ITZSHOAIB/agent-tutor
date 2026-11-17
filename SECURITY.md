# Security policy

## Supported versions

Fixes go to the latest release and `main`.

| Version | Supported |
|---|---|
| Latest release, `main` | ✅ |
| Older releases, forks | ❌ |

## What counts

This repository ships instructions and small Python scripts that an AI agent runs on your machine. Things worth reporting:

- a script that reads or writes outside the paths it is given;
- skill instructions that could lead an agent to run untrusted code, leak files, or publish learner records without being asked;
- a visual template that loads code from somewhere other than the pinned CDNs it names.

## Reporting a vulnerability

Please **don't** open a public issue. Report privately instead:

1. The repository's **Security** tab → **Report a vulnerability**, or
2. The contact listed on [@ITZSHOAIB's GitHub profile](https://github.com/ITZSHOAIB).

Include what the problem is and where, steps to reproduce, the impact you expect, and a fix if you have one. You'll get a reply within a week.
