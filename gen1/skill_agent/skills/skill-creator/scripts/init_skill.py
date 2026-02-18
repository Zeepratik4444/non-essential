#!/usr/bin/env python3
"""
init_skill.py — Initialize a new skill directory with boilerplate structure.

Usage:
    python init_skill.py <skill-name> --path <output-directory>

Example:
    python init_skill.py data-analysis --path ./skills
"""

import argparse
import sys
from pathlib import Path

SKILL_MD_TEMPLATE = """\
---
name: {name}
description: >
  TODO: Describe what this skill does and when to use it.
  Include trigger phrases explicitly, e.g.: "Use when user asks to X, Y, or Z."
  Triggers: "phrase one", "phrase two", "phrase three"
---

# {title}

## Protocol
1. TODO: Step one
2. TODO: Step two
3. TODO: Step three

## Output Format

TODO: Define the exact output structure with a concrete example.

## Rules
- TODO: Hard constraint one
- TODO: Hard constraint two
"""

REFERENCES_PLACEHOLDER = """\
# {title} Reference

TODO: Add reference material, schemas, API docs, or domain knowledge here.
Keep this file focused on a single topic.
Include a table of contents if the file exceeds 100 lines.
"""

def slugify(name: str) -> str:
    return name.lower().strip().replace(" ", "-").replace("_", "-")

def title_case(name: str) -> str:
    return name.replace("-", " ").replace("_", " ").title()

def create_skill(skill_name: str, output_path: Path) -> None:
    name = slugify(skill_name)
    title = title_case(name)
    skill_dir = output_path / name

    if skill_dir.exists():
        print(f"❌ Skill '{name}' already exists at {skill_dir}")
        sys.exit(1)

    # Create directory structure
    skill_dir.mkdir(parents=True)
    (skill_dir / "references").mkdir()
    (skill_dir / "scripts").mkdir()
    (skill_dir / "assets").mkdir()

    # skill.md
    (skill_dir / "skill.md").write_text(
        SKILL_MD_TEMPLATE.format(name=name, title=title),
        encoding="utf-8"
    )

    # Placeholder reference
    (skill_dir / "references" / "reference.md").write_text(
        REFERENCES_PLACEHOLDER.format(title=title),
        encoding="utf-8"
    )

    # Placeholder script
    (skill_dir / "scripts" / "example.py").write_text(
        f'#!/usr/bin/env python3\n"""TODO: Replace with actual utility script for {title}."""\n\nif __name__ == "__main__":\n    print("TODO: implement")\n',
        encoding="utf-8"
    )

    print(f"✅ Skill '{name}' initialized at {skill_dir}")
    print(f"\nStructure:")
    print(f"  {name}/")
    print(f"  ├── skill.md          ← Edit this first")
    print(f"  ├── references/")
    print(f"  │   └── reference.md  ← Replace or delete")
    print(f"  ├── scripts/")
    print(f"  │   └── example.py    ← Replace or delete")
    print(f"  └── assets/           ← Add output files here")
    print(f"\nNext steps:")
    print(f"  1. Edit skill.md — fill in description, protocol, output format")
    print(f"  2. Add real references/scripts/assets or delete the placeholders")
    print(f"  3. Test by calling POST /api/v1/run with a task that should trigger this skill")

def main():
    parser = argparse.ArgumentParser(description="Initialize a new skill directory.")
    parser.add_argument("skill_name", help="Name of the skill (e.g. data-analysis)")
    parser.add_argument("--path", default="./skills", help="Output directory (default: ./skills)")
    args = parser.parse_args()

    output_path = Path(args.path).resolve()
    if not output_path.exists():
        output_path.mkdir(parents=True)

    create_skill(args.skill_name, output_path)

if __name__ == "__main__":
    main()
