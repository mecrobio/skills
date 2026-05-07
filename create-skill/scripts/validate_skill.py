#!/usr/bin/env python3
"""
Agent Skill Validation Script

Validates skill names, descriptions, and directory structures according to
the Agent Skills specification and best practices.
"""

import argparse
import os
import re
import sys
from pathlib import Path
import yaml
import shutil

def validate_skill_name(name):
    """Validate skill name against specification requirements."""
    # Check length first
    if len(name) == 0:
        return False, ["Name cannot be empty"]
    if len(name) > 64:
        return False, ["Name must be 64 characters or less"]
    
    # Check character set
    if not re.match(r'^[a-z0-9-]+$', name):
        return False, ["Name can only contain lowercase letters (a-z), numbers (0-9), and hyphens (-)"]
    
    # Check start/end
    if name.startswith('-') or name.endswith('-'):
        return False, ["Name cannot start or end with a hyphen"]
    
    # Check consecutive hyphens
    if '--' in name:
        return False, ["Name cannot contain consecutive hyphens (--)"]
    
    return True, []

def validate_description(description):
    """Validate skill description."""
    if len(description) == 0:
        return False, ["Description cannot be empty"]
    if len(description) > 1024:
        return False, ["Description must be 1024 characters or less"]
    if not description.strip():
        return False, ["Description cannot be whitespace only"]
    return True, []

def validate_skill_directory(skill_path):
    """Validate that a skill directory follows the expected structure."""
    skill_path = Path(skill_path)
    
    # Check SKILL.md exists
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, ["SKILL.md file is missing"]
    
    # Parse frontmatter
    try:
        with open(skill_md, 'r') as f:
            content = f.read()
            
        # Extract frontmatter
        frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not frontmatter_match:
            return False, ["Invalid frontmatter format - must start with --- and end with ---"]
        
        frontmatter = yaml.safe_load(frontmatter_match.group(1))
        if not frontmatter:
            return False, ["Could not parse frontmatter YAML"]
            
        # Validate required fields
        errors = []
        if 'name' not in frontmatter:
            errors.append("Missing required field: name")
        else:
            valid, name_errors = validate_skill_name(frontmatter['name'])
            if not valid:
                errors.extend([f"name: {error}" for error in name_errors])
                
        if 'description' not in frontmatter:
            errors.append("Missing required field: description")
        else:
            valid, desc_errors = validate_description(frontmatter['description'])
            if not valid:
                errors.extend([f"description: {error}" for error in desc_errors])
        
        # Check if name matches directory
        if 'name' in frontmatter and frontmatter['name'] != skill_path.name:
            errors.append(f"Skill name '{frontmatter['name']}' does not match directory name '{skill_path.name}'")
            
        if errors:
            return False, errors
            
    except Exception as e:
        return False, [f"Error parsing SKILL.md: {str(e)}"]
    
    return True, []

def create_skill_directory(skill_name, description, output_dir=".", license=None, compatibility=None, metadata=None, user_invocable=False):
    """Create a new skill directory with basic structure."""
    skill_path = Path(output_dir) / skill_name
    
    # Validate name first
    valid, errors = validate_skill_name(skill_name)
    if not valid:
        return False, errors
    
    # Validate description
    valid, errors = validate_description(description)
    if not valid:
        return False, errors
    
    # Create directory structure
    try:
        skill_path.mkdir(exist_ok=False)
        (skill_path / "scripts").mkdir(exist_ok=True)
        (skill_path / "references").mkdir(exist_ok=True)
        (skill_path / "assets").mkdir(exist_ok=True)
        
        # Create SKILL.md with frontmatter
        frontmatter = {
            "name": skill_name,
            "description": description
        }
        
        # Set default license to BSD-3-Clause if not provided
        if license:
            frontmatter["license"] = license
        else:
            frontmatter["license"] = "BSD-3-Clause"
            
        # Add user-invocable if specified
        if user_invocable:
            frontmatter["user-invocable"] = True
            
        if compatibility:
            frontmatter["compatibility"] = compatibility
        if metadata:
            frontmatter["metadata"] = metadata
            
        skill_md_content = "---\n" + yaml.dump(frontmatter, default_flow_style=False).strip() + "\n---\n\n"
        skill_md_content += f"# {skill_name.replace('-', ' ').title()}\n\n"
        skill_md_content += f"This skill {description.lower()}\n\n"
        skill_md_content += "## Instructions\n\n"
        skill_md_content += "Add your procedural instructions here...\n\n"
        skill_md_content += "## Gotchas\n\n"
        skill_md_content += "- Add common mistakes and corrections here\n"
        
        with open(skill_path / "SKILL.md", "w") as f:
            f.write(skill_md_content)
            
        return True, [f"Successfully created skill at {skill_path}"]
        
    except Exception as e:
        return False, [f"Error creating skill directory: {str(e)}"]

def main():
    parser = argparse.ArgumentParser(
        description="Agent Skill Validation and Creation Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate a skill name
  python validate_skill.py --name "my-skill"
  
  # Validate an existing skill directory
  python validate_skill.py --validate path/to/skill
  
  # Create a new skill
  python validate_skill.py --create my-skill --description "Does something useful"
        """
    )
    
    parser.add_argument("--name", help="Validate a skill name")
    parser.add_argument("--description", help="Skill description (used with --create)")
    parser.add_argument("--validate", help="Validate an existing skill directory")
    parser.add_argument("--create", help="Create a new skill with the given name")
    parser.add_argument("--output", help="Output directory for new skill (default: current directory)")
    parser.add_argument("--license", help="License for new skill (default: BSD-3-Clause)")
    parser.add_argument("--user-invocable", action="store_true", help="Make skill user-invocable")
    parser.add_argument("--compatibility", help="Compatibility requirements for new skill")
    parser.add_argument("--metadata", help="Metadata for new skill (key=value format)")
    
    args = parser.parse_args()
    
    if args.name:
        # Validate skill name
        valid, errors = validate_skill_name(args.name)
        if valid:
            print(f"✓ Skill name '{args.name}' is valid")
            sys.exit(0)
        else:
            print(f"✗ Invalid skill name '{args.name}':")
            for error in errors:
                print(f"  - {error}")
            sys.exit(1)
    
    elif args.validate:
        # Validate existing skill directory
        valid, errors = validate_skill_directory(args.validate)
        if valid:
            print(f"✓ Skill directory '{args.validate}' is valid")
            sys.exit(0)
        else:
            print(f"✗ Invalid skill directory '{args.validate}':")
            for error in errors:
                print(f"  - {error}")
            sys.exit(1)
    
    elif args.create:
        # Create new skill
        if not args.description:
            print("✗ Error: --description is required when creating a skill")
            sys.exit(1)
            
        # Parse metadata if provided
        metadata = {}
        if args.metadata:
            for item in args.metadata.split(','):
                if '=' in item:
                    key, value = item.split('=', 1)
                    metadata[key.strip()] = value.strip()
        
        success, messages = create_skill_directory(
            skill_name=args.create,
            description=args.description,
            output_dir=args.output or ".",
            license=args.license,
            compatibility=args.compatibility,
            metadata=metadata if metadata else None,
            user_invocable=args.user_invocable
        )
        
        if success:
            for message in messages:
                print(f"✓ {message}")
            sys.exit(0)
        else:
            for message in messages:
                print(f"✗ {message}")
            sys.exit(1)
    
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()