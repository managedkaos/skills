# Details

## Antigravity

Antigravity looks for user-defined and custom skills in the following locations, ordered by scope:

### 1. Global User Skills

- **Path**: `~/.gemini/skills/` (or `~/.agents/skills/`)
- **Scope**: Available across all projects and conversations for your user profile.

### 2. Project / Workspace Skills

- **Path**: `<project-root>/.agents/skills/` (or `<project-root>/.gemini/skills/`)
- **Scope**: Project-scoped skills available only within the specific workspace. These can be committed to repository version control so team members share the same skills.

### 3. Installed Plugin Skills

- **Path**: `~/.gemini/config/plugins/<plugin-name>/skills/`
- **Scope**: Skills bundled and managed by installed Antigravity plugins.

### Built-in System Skills

Built-in skills provided out-of-the-box by Antigravity are located at:

- `~/.gemini/antigravity/builtin/skills/`
