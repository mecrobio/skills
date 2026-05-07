# Agent Skills Specification Summary

This reference provides a concise summary of the Agent Skills specification and best practices.

## Directory Structure

```
skill-name/
├── SKILL.md          # Required: metadata + instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: documentation
└── assets/           # Optional: templates, resources
```

## SKILL.md Format

### Frontmatter Fields

| Field | Required | Constraints |
|-------|----------|-------------|
| `name` | Yes | 1-64 chars, lowercase alphanumeric + hyphens |
| `description` | Yes | 1-1024 chars, describes what + when to use |
| `license` | No | License name or file reference |
| `compatibility` | No | Environment requirements (max 500 chars) |
| `metadata` | No | Arbitrary key-value mapping |
| `allowed-tools` | No | Space-separated pre-approved tools |

### Name Field Rules

**Valid:**
- `pdf-processing`
- `data-analysis` 
- `code-review`

**Invalid:**
- `PDF-Processing` (uppercase)
- `-pdf` (starts with hyphen)
- `pdf--processing` (consecutive hyphens)
- `pdf-` (ends with hyphen)

**Regex pattern:** `^[a-z0-9]([a-z0-9-]{0,62}[a-z0-9])?$`

### Description Best Practices

**Good:** Specific actions + trigger phrases
```yaml
description: Extracts text and tables from PDF files, fills PDF forms, and merges multiple PDFs. Use when working with PDF documents or when the user mentions PDFs, forms, or document extraction.
```

**Poor:** Too vague
```yaml
description: Helps with PDFs.
```

## Best Practices Checklist

### Progressive Disclosure
- [ ] Keep SKILL.md under 500 lines
- [ ] Move detailed reference material to `references/`
- [ ] Load resources on-demand, not upfront

### Content Quality
- [ ] Focus on what agent wouldn't know
- [ ] Provide procedural guidance, not declarations
- [ ] Include gotchas section with common corrections
- [ ] Use templates for structured outputs
- [ ] Add validation loops for self-checking

### Skill Structure
- [ ] Name matches directory name exactly
- [ ] Description is 1-1024 characters
- [ ] YAML frontmatter is valid
- [ ] Instructions are step-by-step procedures
- [ ] Gotchas capture environment-specific issues

## Validation Commands

```bash
# Validate skill name
python scripts/validate_skill.py --name "skill-name"

# Validate existing skill
python scripts/validate_skill.py --validate path/to/skill

# Create new skill
python scripts/validate_skill.py --create skill-name --description "Skill description"
```

## Common Gotchas

- **Name validation**: Must exactly match directory name
- **Description length**: Agents won't load invalid descriptions
- **YAML formatting**: Test with `yaml.lint`
- **Progressive disclosure**: Keep main file concise
- **Trigger phrases**: Include specific keywords for activation