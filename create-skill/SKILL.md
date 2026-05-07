---
name: create-skill
description: Guides users through creating new Agent Skills by gathering requirements, validating structure, and generating complete skill directories. Use when asked to create a new skill, build a skill, or develop an Agent Skill.
user-invocable: true
license: BSD-3-Clause
metadata:
  version: 1.0.0
---

# Create-Skill: Agent Skill Creation Guide

This skill helps you create new Agent Skills by gathering all required information, validating the structure, and generating a complete skill directory following Agent Skills best practices.

## Step-by-Step Skill Creation Process

### 1. Introduction and Requirements Gathering

**Start by explaining the process:**
"I'll guide you through creating a new Agent Skill. This involves:
1. Choosing a skill name (must follow naming conventions)
2. Crafting an effective description
3. Defining the skill's instructions and procedures
4. Adding optional components (scripts, references, assets)
5. Validating and creating the complete skill structure"

**Ask for the skill name first:**
"What would you like to name your new skill? The name must:
- Be 1-64 characters
- Use only lowercase letters (a-z), numbers (0-9), and hyphens (-)
- Not start or end with a hyphen
- Not contain consecutive hyphens (--)"

### 2. Name Validation

**Validate the proposed name using the script:**
```bash
python scripts/validate_skill.py --name "<proposed-name>"
```

**If invalid, provide specific feedback:**
- "Names can only contain lowercase letters, numbers, and hyphens"
- "Names cannot start or end with a hyphen"
- "Names cannot contain consecutive hyphens (--)"
- "Names must be 1-64 characters"

### 3. Description Optimization

**Guide the user to create an effective description:**
"A good description should:
1. **Describe what the skill does** (specific actions/capabilities)
2. **Indicate when to use it** (trigger phrases and scenarios)
3. **Include specific keywords** that help agents identify relevant tasks
4. **Be 1-1024 characters** (concise but informative)"

**Provide examples:**
```yaml
# Good example
description: Extracts text and tables from PDF files, fills PDF forms, and merges multiple PDFs. Use when working with PDF documents or when the user mentions PDFs, forms, or document extraction.

# Poor example (too vague)
description: Helps with PDFs.
```

**Ask for the description:**
"What should your skill do, and when should it be used?"

### 4. Required Fields

**Ask about user-invocable setting:**
"Should this skill be directly invocable by users? (yes/no)"
- If user says "yes" or doesn't specify, set `user-invocable: true`
- If user says "no" or explicitly declines, omit the `user-invocable` field

**Ask about license:**
"What license should this skill use? (e.g., MIT, Apache-2.0, GPL-3.0, or press Enter for BSD-3-Clause default)"
- If user provides a license, use it
- If user doesn't provide one, default to `BSD-3-Clause`

### 5. Optional Fields (Only If Needed)

**Ask about optional fields:**
1. **Compatibility**: "Does this skill have specific requirements? (e.g., 'Requires Python 3.14+ and uv')"
2. **Metadata**: "Any additional metadata? (e.g., author, version)"

**Only include these if the user provides meaningful values.**

### 5. Main Instructions Collection

**Focus on procedural guidance:**
"What specific steps should the agent follow when using this skill? Focus on:
- What the agent wouldn't know without this skill
- Project-specific conventions and tools
- Step-by-step procedures
- Common edge cases and how to handle them"

**Collect instructions in this format:**
```markdown
## How to [achieve the skill's purpose]

1. **Step 1**: [Specific action]
   ```bash
   # Example command if applicable
   ```

2. **Step 2**: [Next action with details]
   - Handle edge case X by doing Y
   - For scenario Z, use approach W
```

### 6. Gotchas Section (Critical for Quality)

**Ask for common mistakes and corrections:**
"What are the 'gotchas' - things that seem reasonable but are wrong in this context?"

**Examples of good gotchas:**
- "The `users` table uses soft deletes - always include `WHERE deleted_at IS NULL`"
- "API endpoint `/health` returns 200 even when database is down - use `/ready` instead"
- "Field names differ across systems: `user_id` in DB, `uid` in auth service, `accountId` in billing API"

### 7. Optional Components

**Ask about additional components:**
1. **Scripts**: "Does this skill need any executable scripts?"
2. **References**: "Should we include detailed reference documentation?"
3. **Assets**: "Are there any templates, schemas, or static resources needed?"

**For each component, gather:**
- Purpose and content
- When the agent should use/load it

### 8. Review and Validation

**Show the complete proposed skill:**
```markdown
---
name: <skill-name>
description: <optimized-description>
user-invocable: true
license: BSD-3-Clause
<compatibility: ...>
---

<Main instructions here>

## Gotchas
<Gotchas list here>
```

**Validate the complete structure:**
```bash
python scripts/validate_skill.py --full <skill-name>
```

### 9. Skill Creation

**Generate the skill directory structure:**
```bash
python scripts/validate_skill.py --create <skill-name> --description "<description>" <other-options>
```

**Confirm creation:**
"I've created your new skill at `<skill-name>/` with the following structure:
```
<skill-name>/
├── SKILL.md          # Main skill file
├── scripts/          # Executable scripts
├── references/       # Detailed documentation
└── assets/           # Templates and resources
```

## Gotchas for Skill Creation

- **Name validation**: The name must exactly match the directory name
- **Description length**: Must be 1-1024 characters - agents won't load skills with invalid descriptions
- **YAML formatting**: Frontmatter must be valid YAML - test with `yaml.lint`
- **Progressive disclosure**: Keep SKILL.md under 500 lines - move details to references/
- **Trigger phrases**: Include specific keywords in description for reliable activation

## Validation and Testing

**Always validate before finalizing:**
1. Run the validation script
2. Check all required fields are present
3. Verify the description is trigger-rich
4. Test with sample inputs

**Test the skill by:**
1. Placing it in a skills directory
2. Asking the agent to perform the skill's task
3. Verifying it activates and executes correctly
