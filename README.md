# Skills

AI skills and other related content.

## Skill Specifications

See [https://agentskills.io/specifications](https://agentskills.io/specifications) for the full skill specification.

At the very least the skill should:

1. Be stored in a lower-cased directory named after the skill.
2. Contain a `SKILL.md` file with the following frontmatter entries:

    - **name**: The name of the skill. Max 64 characters. Lowercase letters, numbers, and hyphens only. Must not start or end with a hyphen.
    - **description**: A description of what the skill does and when to use it. Max 1024 characters. Non-empty.


## Skill Index

This repo contains the following skills:

<!-- skills-index-start -->

| Skill | Description |
| --- | --- |
| [hello-skill](hello-skill/) | A minimal example skill that responds with a greeting. |
| [makefile-help](makefile-help/) | Annotate a Makefile with self-documenting help targets. Adds a `help` target as the default and appends inline descriptions to every user-facing target. |

<!-- skills-index-end -->
