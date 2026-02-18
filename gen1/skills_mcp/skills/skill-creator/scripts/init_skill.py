#!/usr/bin/env python3
"""
init_skill.py — Scaffold a new skill directory.

Usage:
    python init_skill.py <skill-name> --path ./skills
"""

import argparse
import sys
from pathlib import Path

SKILL_MD_TEMPLATE = """\
---
name: {name}
description: >
  TODO: What this skill does and when to use it.
  Include trigger phrases: "phrase one", "phrase two"
---

# {title}

## Protocol
1. TODO: Step one
2. TODO: Step two
3. TODO: Step three

## Output Format

TODO: Concrete example of expected output.

## Rules
- TODO: Hard constraint one
- TODO: Hard constraint two
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

    skill_dir.mkdir(parents=True)
    (skill_dir / "references").mkdir()
    (skill_dir / "scripts").mkdir()
    (skill_dir / "assets").mkdir()

    (skill_dir / "skill.md").write_text(
        SKILL_MD_TEMPLATE.format(name=name, title=title), encoding="utf-8"
    )

    print(f"✅ Skill '{name}' scaffolded at {skill_dir}")
    print(f"\n{name}/")
    print(f"  ├── skill.md      ← Edit this first")
    print(f"  ├── references/")
    print(f"  ├── scripts/")
    print(f"  └── assets/")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("skill_name")
    parser.add_argument("--path", default="./skills")
    args = parser.parse_args()
    create_skill(args.skill_name, Path(args.path).resolve())

if __name__ == "__main__":
    main()
