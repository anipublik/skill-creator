#!/usr/bin/env python3
"""
scaffold_skills.py - generate starter folders for a batch of skills from one spec file.

Why this is a script and not prose: scaffolding the same directory structure and
boilerplate files by hand for every skill in a batch is repetitive and error-prone.
This does it once, consistently, so the AI's time goes into actual content instead
of retyping the same tree ten times.

Contract:
  Input:  a JSON file containing a list of skill specs:
            [
              {
                "name": "skill-name",              (required - folder name and `name:` field)
                "description": "...",              (required - `description:` field)
                "references": ["topic-a", "topic-b"],  (optional - reference file stems)
                "scripts": ["do-thing"],               (optional - script file stems)
                "assets": ["template.docx"]             (optional - asset filenames)
              },
              ...
            ]
  Output: for each spec, a folder `<out>/<name>/` containing:
            - SKILL.md            (name + description filled in, body left as prompts)
            - references/<x>.md   for each entry in "references"
            - scripts/<x>.py      for each entry in "scripts"
            - assets/<x>          empty placeholder for each entry in "assets"
          Prints one line per skill created. Skips (does not overwrite) any
          folder that already exists.

Usage:
  python3 scaffold_skills.py specs.json --out ./skills

Dependencies: none (standard library only)

Fallback for AIs that cannot run code:
  Build each folder by hand from templates/SKILL.template.md,
  templates/reference.template.md, and templates/script.template.py, filling in
  name/description per spec. See "Building many skills at once" in SKILL.md.
"""

import argparse
import json
import sys
from pathlib import Path

def yaml_quote(s):
    """Double-quoted YAML scalar, safe for any content. Stdlib only, no
    PyYAML dependency. Plain (unquoted) YAML scalars break on embedded
    colons, leading quotes, or several other characters that show up
    routinely in real skill descriptions - the field this is quoting is
    the one place a colon or a quoted trigger phrase is most likely to
    appear, per SKILL.md Phase 3. Always quoting removes the ambiguity
    instead of trying to detect which strings need it."""
    escaped = s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    return f'"{escaped}"'


SKILL_TEMPLATE = """---
name: {name}
description: {description}
---

# {title}

[One or two sentences: what this does and the mindset to bring to it.]

## When to use which approach

[Delete this section if the skill has no variants. Otherwise: the decision logic for picking a path or a reference file. "Determine X from the request, then read the matching reference and follow it; do not read the others."]

## Workflow

[The ordered steps. Write in the imperative. Call out decision points. Flag the places people usually get it wrong, and say why the right way is right.]

1. [Step one.]
2. [Step two.]
3. [Step three.]

## Output format

[The exact shape of a good result, shown concretely.]

## Examples

**Example 1:**
Input: [realistic input]
Output: [what the skill should produce for it]
{resources_section}"""

REFERENCE_TEMPLATE = """# {title}

[One line on what this reference covers and when the skill body should send the AI here.]

## Contents

- Section one
- Section two

## Section one

[Deep detail that would bloat the body if it lived there - edge cases, full specs, lookup tables.]

## Section two

[...]
"""

SCRIPT_TEMPLATE = '''#!/usr/bin/env python3
"""
{stem} - one line on what deterministic job this does.

Contract:
  Input:  [what it takes - args, stdin, a file path.]
  Output: [what it produces - stdout, a file, an exit code.]

Dependencies: [none, or list]

Fallback for AIs that cannot run code:
  [point back to the equivalent prose logic in SKILL.md or a reference]
"""

import sys


def main(argv):
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
'''


def build_resources_section(refs, scripts, assets):
    if not (refs or scripts or assets):
        return ""
    lines = ["\n## Resources\n"]
    for r in refs:
        lines.append(f"- `references/{r}.md` - [what it covers; read it when ...]")
    for s in scripts:
        lines.append(f"- `scripts/{s}.py` - [what it does; run it when ...]")
    for a in assets:
        lines.append(f"- `assets/{a}` - [what it is; use it as ...]")
    return "\n".join(lines) + "\n"


def titleize(stem):
    return stem.replace("-", " ").replace("_", " ").title()


def scaffold_one(spec, out_dir):
    name = spec["name"]
    description = spec["description"]
    refs = spec.get("references", [])
    scripts = spec.get("scripts", [])
    assets = spec.get("assets", [])

    root = out_dir / name
    if root.exists():
        print(f"skip  {name}: {root} already exists")
        return

    root.mkdir(parents=True)
    resources_section = build_resources_section(refs, scripts, assets)
    (root / "SKILL.md").write_text(
        SKILL_TEMPLATE.format(
            name=yaml_quote(name),
            description=yaml_quote(description),
            title=titleize(name),
            resources_section=resources_section,
        )
    )

    if refs:
        ref_dir = root / "references"
        ref_dir.mkdir()
        for r in refs:
            (ref_dir / f"{r}.md").write_text(REFERENCE_TEMPLATE.format(title=titleize(r)))

    if scripts:
        script_dir = root / "scripts"
        script_dir.mkdir()
        for s in scripts:
            (script_dir / f"{s}.py").write_text(SCRIPT_TEMPLATE.format(stem=s))

    if assets:
        asset_dir = root / "assets"
        asset_dir.mkdir()
        for a in assets:
            (asset_dir / a).touch()

    print(f"made  {name}: {root}")


def main(argv):
    parser = argparse.ArgumentParser(description="Scaffold folders for a batch of skills.")
    parser.add_argument("specs", help="Path to a JSON file with a list of skill specs.")
    parser.add_argument(
        "--out",
        default=".",
        help="Directory to create skill folders in (default: current directory).",
    )
    args = parser.parse_args(argv)

    specs_path = Path(args.specs)
    if not specs_path.exists():
        print(f"error: {specs_path} not found", file=sys.stderr)
        return 1

    try:
        specs = json.loads(specs_path.read_text())
    except json.JSONDecodeError as e:
        print(f"error: invalid JSON in {specs_path}: {e}", file=sys.stderr)
        return 1

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    for spec in specs:
        if "name" not in spec or "description" not in spec:
            print(f"skip: spec missing name/description: {spec}", file=sys.stderr)
            continue
        scaffold_one(spec, out_dir)

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
