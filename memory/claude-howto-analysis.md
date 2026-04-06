# Claude Howto Analysis - Complete Reference

This document captures key learnings from the Claude Howto guide for applying to our bot development.

## Overview

The Claude Howto guide covers 10 modules:
1. **Slash Commands** - User-initiated shortcuts
2. **Memory** - Persistent context via CLAUDE.md files
3. **Skills** - Reusable autonomous capabilities
4. **Subagents** - Delegated AI agents
5. **MCP** - External data access
6. **Hooks** - Event-driven automation
7. **Plugins** - Bundled extensions
8. **Checkpoints** - Session rewinding
9. **Advanced Features** - Planning, extended thinking, permissions
10. **CLI** - Command reference

---

## Key Patterns to Apply

### 1. Memory (CLAUDE.md) - Critical for Bot Context

**Hierarchy (highest to lowest):**
```
Managed Policy > Project Memory (.claude/CLAUDE.md) > User Memory (~/.claude/CLAUDE.md) > Auto Memory
```

**Key Patterns:**
```markdown
# Project root CLAUDE.md
## Project Overview
- Tech Stack, team size, conventions

## Development Standards
Naming, git workflow, testing requirements

## Quick Commands
npm run dev, npm test, etc.

## Known Issues
Workarounds for common problems
```

**Quick memory update during conversation:**
```markdown
# new rule into memory
Your rule here
```

**Memory imports:**
```markdown
@docs/architecture.md
@~/shared/config.md
```

### 2. Skills - Automate Repetitive Tasks

Skills are stored in:
- Project: `.claude/skills/<skill-name>/SKILL.md`
- User: `~/.claude/skills/<skill-name>/SKILL.md`

**SKILL.md Format:**
```yaml
---
name: skill-name
description: What it does AND when to use it (triggers)
---

# Skill Name

## Instructions
Step-by-step guidance

## Templates
Copy-paste code
```

**Key Fields:**
- `name`: lowercase with hyphens
- `description`: Include trigger terms for auto-invocation
- `context: fork`: Run in isolated subagent
- `disable-model-invocation: true`: User-only invocation
- `allowed-tools`: Restrict tool access

**String substitutions:**
```yaml
$ARGUMENTS      # All arguments passed
$ARGUMENTS[0]   # First argument
${CLAUDE_SKILL_DIR}  # Skill directory path
!`command`       # Dynamic context injection
```

### 3. Subagents - Specialized AI Workers

**File Location:** `.claude/agents/<name>.md`

**Frontmatter Format:**
```yaml
---
name: agent-name
description: When to invoke (include "use PROACTIVELY" to encourage auto-use)
tools: Read, Grep, Bash
model: sonnet
skills: skill1, skill2
memory: project  # user, project, or local
background: false
effort: high
---

System prompt here...
```

**Built-in Agents:**
- `general-purpose` - Complex multi-step tasks
- `Explore` - Read-only code analysis (Haiku)
- `Plan` - Research for plan mode
- `Bash` - Isolated terminal commands

### 4. Hooks - Event-Driven Automation

**Configuration:** In `settings.json` under `hooks` key

**Event Types:**
- `PreToolUse` - Validate/modify before execution
- `PostToolUse` - Verify/log after execution
- `Stop` - Task completion checking
- `SessionStart`, `SessionEnd`
- `UserPromptSubmit` - Prompt validation

**Example Hook (PreToolUse for Bash validation):**
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "./hooks/validate-bash.sh",
        "timeout": 30
      }]
    }]
  }
}
```

**Hook types:** `command` (bash), `prompt` (LLM), `http` (webhook), `agent` (subagent)

### 5. MCP - External Integrations

**Configuration:** `.mcp.json` in project root

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-github"],
      "env": { "GITHUB_TOKEN": "${GITHUB_TOKEN}" }
    }
  }
}
```

**Transport types:** `stdio` (local), `http` (remote), `ws` (WebSocket)

**Env var expansion:** `${VAR}` or `${VAR:-default}`

---

## Templates by Use Case

### Project Memory Template
```markdown
# Project Configuration

## Project Overview
- **Name**: Project name
- **Tech Stack**: Node.js, PostgreSQL, React
- **Team Size**: 5 developers

## Development Standards
### Naming Conventions
- Files: kebab-case
- Functions: camelCase
- Constants: UPPER_SNAKE_CASE

### Git Workflow
- Branch: feature/description
- Commits: conventional commits
- PR required before merge

### Commands
| Command | Purpose |
|---------|---------|
| npm run dev | Start dev server |
| npm test | Run tests |

## Known Issues
- PostgreSQL pooling issue workaround in docs/dev-notes.md
```

### Skill Template
```yaml
---
name: my-skill
description: Does X. Use when user mentions X, asks about X, or needs X.
---

# My Skill

## When to Use
Triggered when...

## Workflow
1. Step one
2. Step two

## Templates
```code here
```
```

### Subagent Template
```yaml
---
name: my-agent
description: Expert in X. Use PROACTIVELY when working with X.
tools: Read, Grep, Glob, Bash
model: sonnet
---

# My Agent

You are an expert in X...

## Approach
1. First do...
2. Then do...

## Output Format
Provide findings in this format...
```

### Hook Template (Bash validation)
```python
#!/usr/bin/env python3
import json
import sys
import re

BLOCKED = [r"\brm\s+-rf\s+/", r"\bsudo\s+rm"]

def main():
    data = json.load(sys.stdin)
    if data.get("tool_name") != "Bash":
        sys.exit(0)
    
    cmd = data.get("tool_input", {}).get("command", "")
    for pattern, msg in BLOCKED:
        if re.search(pattern, cmd):
            print(msg, file=sys.stderr)
            sys.exit(2)  # Block
    sys.exit(0)

if __name__ == "__main__":
    main()
```

---

## Best Practices

### Memory
- ✅ Use specific, actionable rules
- ✅ Organize with clear markdown sections
- ✅ Include common commands
- ❌ Don't store secrets
- ❌ Don't duplicate content (use imports)
- ❌ Don't exceed 500 lines per file

### Skills
- ✅ One skill = one capability
- ✅ Include trigger terms in description
- ✅ Keep SKILL.md under 500 lines
- ✅ Reference supporting files with relative paths
- ❌ Don't make skills too broad

### Subagents
- ✅ Write detailed prompts with priorities
- ✅ Specify output format
- ✅ Grant minimal necessary tools
- ✅ Use `use PROACTIVELY` in description
- ❌ Don't give unnecessary tool access

### Hooks
- ✅ Always read JSON from stdin
- ✅ Return exit code 0 for allow, 2 for block
- ✅ Quote shell variables
- ❌ Don't trust input blindly

---

## Common Pitfalls

1. **Memory overload** - Too many rules, not organized
2. **Skill description too vague** - Claude can't auto-invoke
3. **Subagent tool over-granting** - Security risk
4. **Hook JSON parsing** - Must read from stdin, not args
5. **Context pollution** - Using subagents for simple tasks

---

## OpenClaw-Specific Application

Based on the guide, here's what we can apply:

### 1. Memory for Bot Context
Our bots should have organized memory files documenting:
- Bot capabilities and limitations
- Team conventions
- Project structure
- Common workflows

### 2. Skills for Repetitive Tasks
Create skills for:
- Code review patterns
- Git workflow automation
- Documentation generation
- Testing workflows

### 3. Subagents for Specialization
Implement subagents for:
- Code reviewer (proactive after changes)
- Debugger (on errors)
- Documentation writer
- Security auditor

### 4. Hooks for Automation
Add hooks for:
- Pre-commit validation
- Code formatting
- Security scanning
- Test running

### 5. MCP for External Access
Configure MCP for:
- GitHub integration
- Database queries
- Slack/messaging

---

## Quick Reference - File Locations

| Feature | Project Path | User Path |
|---------|-------------|-----------|
| Memory | `.claude/CLAUDE.md` or `./CLAUDE.md` | `~/.claude/CLAUDE.md` |
| Rules | `.claude/rules/*.md` | `~/.claude/rules/*.md` |
| Skills | `.claude/skills/<name>/SKILL.md` | `~/.claude/skills/<name>/SKILL.md` |
| Agents | `.claude/agents/<name>.md` | `~/.claude/agents/<name>.md` |
| Hooks | `.claude/settings.json` | `~/.claude/settings.json` |
| MCP | `.mcp.json` | `~/.claude.json` |

---

## Key CLI Commands

```bash
claude                    # Interactive mode
claude -p "query"        # Print mode (non-interactive)
claude -c                 # Continue last session
claude -r "session"       # Resume session
claude --agents           # List agents
claude mcp                # Manage MCP servers
claude plugin             # Manage plugins
/plan                     # Planning mode
/rewind                   # Rewind to checkpoint
/memory                   # Edit memory
```

---

*Generated from Claude Howto guide analysis - April 2026*
