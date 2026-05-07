---
name: create-agent
description: Guides users through creating Mistral Vibe agent and subagent configurations in TOML format, including custom system prompts. Use when asked to create a new agent, build an agent, or set up a Mistral Vibe agent or subagent.
user-invocable: true
license: BSD-3-Clause
metadata:
  version: 1.0.0
---

# Create-Agent: Mistral Vibe Agent and Subagent Configuration Guide

This skill helps you create Mistral Vibe agent or subagent configurations by gathering requirements and generating valid TOML configuration files, including writing custom system prompts to disk.

**Important**: Each TOML file in `~/.vibe/agents/` defines exactly one agent or subagent. All configuration fields are at the root level of the file.

## Step-by-Step Configuration Process

### 1. Introduction

**Start by explaining the process:**
"I'll guide you through creating a new Mistral Vibe configuration. This involves:
1. Choosing between an agent or a subagent
2. Providing a display name and description
3. Selecting a safety level
4. Configuring tool access and approval settings
5. Optionally creating and writing a custom system prompt (markdown file) to disk
6. Generating the TOML configuration file with system_prompt_id reference"

**Explain the configuration file:**
"Mistral Vibe configurations are TOML files stored in `~/.vibe/agents/`. Each `.toml` file defines exactly one agent or subagent, with all fields at the root level.

Custom system prompts are markdown files stored in `~/.vibe/prompts/` and referenced by ID (without the `.md` extension)."

### 2. Determine Agent Type

**Ask if this should be a subagent:**
"Will this be a **subagent** for task delegation, or a regular **agent**? (subagent/agent)"

**Explain the difference:**

**Regular Agent:**
- Can interact directly with users
- Can ask questions using `ask_user_question` tool
- Can delegate tasks to subagents using `task` tool
- Maintains session logs

**Subagent:**
- Designed for task delegation from main agents
- Cannot ask questions (no interactive input)
- Runs independently and returns results as text only
- Runs in-memory without saving session logs
- Useful for parallel work, specialized tasks, and safety isolation

**Recommendation:**
"Use a regular **agent** for user-facing configurations. Use a **subagent** for specialized background tasks like code exploration, research, or parallel processing."

**Set agent_type internally:**
- If subagent: `agent_type = "subagent"` will be added to config
- If agent: no agent_type field needed

### 3. Gather Basic Information

**Ask for display name:**
"What should be the display name for your agent/subagent? This is how it will appear in selections."

**Ask for description:**
"What does this agent/subagent do? Provide a clear, concise description (1-1024 characters). This helps users understand when to use it."

**Validate description:**
- Must be 1-1024 characters
- If too short: "The description is too short. Please provide more detail about what it does."
- If too long: "The description exceeds 1024 characters. Please make it more concise."

### 4. Configure Safety Level

**Ask about safety level:**
"What safety level should this have? Choose from:
- **safe**: Visual indicator for safe, read-only operations
- **neutral**: Default visual indicator
- **destructive**: Visual indicator for potentially destructive operations
- **yolo**: Visual indicator for unrestricted mode"

**Important note:**
"This field currently changes only the user input border color to visually inform you of the safety level. **It does NOT implement actual safety measures.** You must configure appropriate tool permissions separately via enabled_tools."

**Recommendation based on type:**
- For read-only agents/subagents: `safe`
- For most configurations: `neutral`
- For agents with file editing/deletion: `destructive`
- For unrestricted access: `yolo` (use with extreme caution)

### 5. Configure Tool Access

**Ask if tool access is needed:**
"Should this have access to tools? (yes/no)"

**If yes:**
"Which tools should it be able to use? Provide a comma-separated list or say 'all available'."

**Common tools to mention** (filtered by type):
- **For both agents and subagents:** `read_file`, `grep`, `bash` (read-only), `python` (analysis only)
- **For agents only:** `ask_user_question`, `task` (to delegate to subagents), `write_file`
- **For web-enabled:** `web_search`, `web_fetch`

**Note for subagents:**
"Subagents cannot ask questions, so they cannot use the `ask_user_question` tool. They also cannot delegate to other subagents."

**If user says 'all available':**
"This will give access to all currently installed tools. For subagents, note that some tools like `ask_user_question` and `task` will not work."

**Ask about disabled tools:**
"Should any specific tools be explicitly disabled for this configuration? (yes/no)"

**If yes:**
"Which tools should be disabled? Provide a comma-separated list."

**Ask about per-tool permissions:**
"Do you need to override the default permission for any specific tools? (yes/no)"

**If yes:**
"For each tool, specify 'always' (no prompt) or 'ask' (prompt user). Example: `bash=always, write_file=ask`"

### 6. Configure Approval Settings

**Ask about auto-approval:**
"Should this auto-approve tool usage without user confirmation? (yes/no)"

**Explain the implications:**
- If `auto_approve = true`: Tools execute immediately without prompting. Use for trusted, well-tested configurations only.
- If `auto_approve = false` (or omitted): User will be prompted to approve each tool usage. Recommended for development and testing.

**Recommendation:**
"For new configurations, I recommend setting `auto_approve = false` initially. Change to `true` after thorough testing, especially for agents/subagents with destructive capabilities."

### 7. Optional: Custom System Prompt

**Ask if custom system prompt is needed:**
"Does this need a custom system prompt? (yes/no)"

**If user says yes:**
"I can help you create a custom system prompt. Custom prompts are stored in `~/.vibe/prompts/` and referenced by ID in the agent configuration."

**Evaluate the user's initial prompt description:**

**Ask for prompt content:**
"What should the system prompt contain? Provide the complete text that will guide the agent's behavior."

**If the description is vague** (e.g., "be helpful", "act as an expert"):
"This prompt is too vague and won't effectively guide the agent. To create an effective system prompt, I need more details. Consider:

- **Persona**: What role should the agent play? (e.g., 'You are a senior Python developer')
- **Tone**: Formal, casual, technical, conversational?
- **Focus**: What should it focus on? (e.g., 'specialize in security code reviews')
- **Format**: How should it respond? (e.g., 'provide detailed explanations with code examples')
- **Constraints**: Any topics to avoid? Specific boundaries? (e.g., 'never execute user-provided code without review')
- **Workflows**: Step-by-step procedures the agent should follow
- **Examples**: What does ideal input/output look like?"

**Provide examples of good system prompts:**
```text
# Too Vague:
"You are a helpful assistant"

# Better for a code review agent:
"You are a senior Python developer specializing in code quality. Review code for bugs, performance issues, and style problems. Provide specific, actionable feedback with code examples. Use markdown formatting."

# Even Better for a security agent:
"You are a security auditor with 10+ years of experience. When analyzing code:
1. Check for OWASP Top 10 vulnerabilities
2. Identify security anti-patterns and hardcoded secrets
3. Assess dependency vulnerabilities
4. Provide patched code with clear explanations
5. Reference relevant CVE entries when applicable
6. Always warn about potential risks before suggesting fixes

Format all responses using markdown with clear sections."
```

**If the description is detailed:**
Summarize the key elements and confirm the prompt content.

**Ask for prompt ID:**
"What ID should I use for this prompt? This will be the filename (without extension) in `~/.vibe/prompts/`.

Use lowercase with hyphens, e.g., `code-reviewer`, `security-auditor`."

**Generate the prompt file:**
Write the prompt content to `~/.vibe/prompts/<prompt-id>.md`

**Confirm prompt creation:**
"I've written the custom system prompt to `~/.vibe/prompts/<prompt-id>.md`."

**Set system_prompt_id for agent:**
The agent TOML will include: `system_prompt_id = "<prompt-id>"`

**If user says no to custom prompt:**
No system_prompt_id field will be included. The agent will use the default system prompt.

### 8. Generate Configuration

**Create the TOML file structure:**

Minimal configuration:
```toml
display_name = "<display-name>"
description = "<description>"
```

Full configuration for regular agent:
```toml
display_name = "<display-name>"
description = "<description>"
safety = "<safety-level>"
auto_approve = <true/false>
enabled_tools = [<tool-list>]
<disabled_tools-line-if-applicable>
<system_prompt_id-line-if-applicable>
<tool-permissions-if-applicable>
```

Full configuration for subagent:
```toml
display_name = "<display-name>"
description = "<description>"
safety = "<safety-level>"
auto_approve = <true/false>
enabled_tools = [<tool-list>]
disabled_tools = [<disabled-list>]
agent_type = "subagent"
<system_prompt_id-line-if-applicable>
<tool-permissions-if-applicable>
```

**Note**: All fields are at the root level - there is no `[agent]` section header.

### 9. Review and Confirm

**Show the proposed configuration:**
```toml
# ~/.vibe/agents/<filename>.toml
display_name = "<display-name>"
description = "<description>"
safety = "<safety-level>"
auto_approve = <true/false>
<enabled_tools-line>
<agent_type-line-for-subagent>
<system_prompt_id-line-if-applicable>
```

**Also show any custom prompt to be created:**
```
Custom prompt file: ~/.vibe/prompts/<prompt-id>.md
Content: <prompt-content-preview>
```

**Ask for confirmation:**
"Here is the proposed configuration for <agent/subagent>. Please review:
- Type: <agent/subagent>
- Display name: <display-name>
- Description: <description>
- Safety level: <safety-level>
- Auto-approve: <true/false>
- Enabled tools: <tool-list>
- Disabled tools: <disabled-list>
- Custom prompt: <yes/no> (<prompt-id>)
- Tool permissions: <permissions-list>

Is this correct? (yes/no)"

**If yes:**
"I'll create:
1. Prompt file at `~/.vibe/prompts/<prompt-id>.md` (if custom prompt)
2. Configuration file at `~/.vibe/agents/<filename>.toml`"

**If no:**
"What would you like to change? You can modify any of the fields or the custom prompt content."

### 10. Save Configuration

**Create the files:**
1. If custom prompt: Write prompt content (as markdown) to `~/.vibe/prompts/<prompt-id>.md`
2. Write agent configuration to `~/.vibe/agents/<filename>.toml`

**Ensure proper TOML formatting:**
- Use valid TOML syntax
- Escape quotes in strings: `"It's a test"`
- Use arrays for tools: `["read_file", "grep"]`
- Use triple-quoted strings for multi-line descriptions if needed
- Ensure all fields are at root level (no section headers)

**Filename conventions:**
- Agent config: lowercase with hyphens in `~/.vibe/agents/`
- Prompt file: lowercase with hyphens in `~/.vibe/prompts/`

**Confirm creation:**
"I've created your configuration:

<custom-prompt-confirmation>

Agent configuration at `~/.vibe/agents/<filename>.toml`.

For **agents**: You can now select it in Mistral Vibe using:
```bash
vibe --agent <filename>
```

For **subagents**: This can be used by other agents via the `task` tool for delegation.

Remember to:
1. Test with `auto_approve = false` first
2. Reload Mistral Vibe or restart to see the new configuration
3. Review behavior before enabling auto-approve
4. The safety field is visual only - configure actual safety via enabled_tools"

## Configuration Reference

### File Locations
| File Type | Location | Purpose |
|-----------|----------|---------|
| Agent/Subagent configs | `~/.vibe/agents/` | Define agent/subagent behavior and tools |
| Custom prompts | `~/.vibe/prompts/` | System prompt markdown files referenced by system_prompt_id |

### Required Fields
| Field | Type | Description |
|-------|------|-------------|
| display_name | string | Human-readable name (required) |
| description | string | What it does (1-1024 chars) |

### Optional Fields
| Field | Type | Options | Default | Description |
|-------|------|---------|---------|-------------|
| safety | string | safe, neutral, destructive, yolo | - | Visual safety indicator (no enforcement) |
| auto_approve | boolean | true, false | false | Skip tool usage confirmation |
| enabled_tools | array | tool names | all | Tools available to use |
| disabled_tools | array | tool names | none | Tools explicitly disabled |
| system_prompt_id | string | prompt ID | - | ID of custom markdown prompt in `~/.vibe/prompts/` (without `.md` extension) |
| agent_type | string | "subagent" | - | Mark as subagent for delegation |

**Tool Permissions**: You can override tool permissions with `[tools.<tool-name>]` sections:
```toml
[tools.bash]
permission = "always"
[tools.read_file]
permission = "ask"
```
Permission options: `"always"` (execute without prompt) or `"ask"` (prompt user).

### Safety Levels
- **safe**: Visual indicator for safe operations
- **neutral**: Default visual indicator
- **destructive**: Visual indicator for destructive operations
- **yolo**: Visual indicator for unrestricted mode

**Important**: The safety field only changes the user input border color. It does NOT enforce any restrictions. Enforce actual safety through enabled_tools permissions.

## Agent vs Subagent Comparison

| Feature | Agent | Subagent |
|---------|-------|----------|
| User interaction | Yes | No (text only) |
| Can ask questions | Yes (`ask_user_question`) | No |
| Can delegate tasks | Yes (`task` tool) | No |
| Session logging | Yes | No (in-memory) |
| Use case | Direct user interaction | Background tasks, delegation |

## Gotchas

- **TOML syntax**: TOML is sensitive to quotes and special characters. Validate your TOML file.
- **Root level fields**: All fields must be at the root level - do NOT use section headers like `[agent]`.
- **Tool names**: Use exact tool names as registered in Mistral Vibe.
- **File location - agents**: Configurations MUST be in `~/.vibe/agents/` with `.toml` extension.
- **File location - prompts**: Custom prompts MUST be in `~/.vibe/prompts/` with `.md` extension.
- **File naming**: Filenames are internal IDs. Use lowercase with hyphens.
- **Description length**: Keep under 1024 characters.
- **No prompt field**: There is NO `prompt` field in agent TOML. Use `system_prompt_id` to reference prompts in `~/.vibe/prompts/`.
- **Write prompts to disk**: Custom system prompts must be written to `~/.vibe/prompts/<id>.md` and referenced via system_prompt_id (without the `.md` extension).
- **Testing**: Always test with `auto_approve = false` first.
- **One per file**: Each TOML file defines exactly one agent or subagent.
- **Safety is visual only**: Enforce actual safety through tool permissions, not the safety field.
- **Subagent limitations**: Subagents cannot use `ask_user_question` or `task` tools.
- **Prompt directory**: Create the `~/.vibe/prompts/` directory if it doesn't exist.

## Example Configurations

### Regular Agent
```toml
# ~/.vibe/agents/code-reviewer.toml
display_name = "Code Reviewer"
description = "Reviews Python code for quality, bugs, and security issues"
safety = "neutral"
auto_approve = false
enabled_tools = ["read_file", "grep"]
```

### Subagent
```toml
# ~/.vibe/agents/research.toml
display_name = "Research"
description = "Read-only subagent for research tasks"
safety = "safe"
agent_type = "subagent"
enabled_tools = ["grep", "read_file"]
```

### Agent with Custom System Prompt
```toml
# ~/.vibe/agents/custom-prompt-agent.toml
display_name = "Custom Prompt Agent"
description = "Uses a custom system prompt"
safety = "neutral"
auto_approve = false
enabled_tools = ["read_file"]
system_prompt_id = "code-reviewer"
```

With corresponding prompt file:
```md
# ~/.vibe/prompts/code-reviewer.md
You are a senior Python developer specializing in code quality.
Review code for bugs, performance issues, and style problems.
Provide specific, actionable feedback with code examples.
```

### Agent with Tool Restrictions
```toml
# ~/.vibe/agents/secure-agent.toml
display_name = "Secure Agent"
description = "Agent with restricted tool access"
safety = "safe"
auto_approve = false
enabled_tools = ["read_file", "grep", "bash"]
disabled_tools = ["write_file", "search_replace"]

# Override specific tool permissions
[tools.bash]
permission = "ask"
```
