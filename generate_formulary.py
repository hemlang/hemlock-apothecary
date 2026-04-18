#!/usr/bin/env python3
"""Generate the Formulary: a stdlib-focused SFT dataset for Hemlock-Apothecary-7B.

A formulary is a pharmacological reference listing exact compositions and
dosages. This dataset is the same thing for Hemlock's standard library:
realistic programs showing the right imports, right API names, and right
composition for each @stdlib/<module>.

Designed to be trained alongside Hemlock-Codex's translation/generation SFT
to close the L2-Stdlib gap measured on hembench (Codex-7B Q8_0 baseline 40%
on L2 zero-shot; the model hallucinates method names and omits imports).

For each .hml under hemlock/stdlib/<module>/<task>.hml it emits up to 3 rows:
  - hinted:        prompt names "@stdlib/<module>", teaches correct import syntax
  - unhinted:      prompt omits the module name, teaches module recognition
  - import-recall: prompt asks "which functions do I need to import"
"""

import json
import random
from pathlib import Path

from formulary_descriptions import DESCRIPTIONS

SEED = 42
random.seed(SEED)

REPO_ROOT = Path(__file__).parent
STDLIB_DIR = REPO_ROOT / "hemlock" / "stdlib"
OUTPUT_FILE = REPO_ROOT / "hemlock_apothecary_formulary.jsonl"

# All templates end in an imperative slot so descriptions stay in one form.
# Descriptions should be imperative phrases, e.g. "parse a JSON record and ...".

HINTED_TEMPLATES = [
    "Using @stdlib/{module}, write a Hemlock program to {desc}.",
    "Write a Hemlock program to {desc}. Use @stdlib/{module}.",
    "In Hemlock (importing from @stdlib/{module}), {desc}.",
]

UNHINTED_TEMPLATES = [
    "Write a Hemlock program to {desc}.",
    "In Hemlock, {desc}.",
    "Solve this in Hemlock: {desc}.",
]

IMPORT_TEMPLATES = [
    "What imports do I need from @stdlib/{module} to {desc}? Write the full Hemlock program.",
    "Show the imports and Hemlock code to {desc}.",
]


def extract_imports(code: str) -> list[str]:
    return [line.strip() for line in code.splitlines() if line.strip().startswith("import ")]


def read_stripped(path: Path) -> str:
    lines = [l.rstrip() for l in path.read_text(encoding="utf-8").splitlines()]
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines)


def main():
    rows = []
    missing_desc = []
    per_module = {}

    for hml_path in sorted(STDLIB_DIR.rglob("*.hml")):
        module = hml_path.parent.name
        task = hml_path.stem
        code = read_stripped(hml_path)
        imports = extract_imports(code)

        desc = DESCRIPTIONS.get((module, task))
        if desc is None:
            missing_desc.append(f"{module}/{task}")
            continue

        hinted = random.choice(HINTED_TEMPLATES).format(module=module, desc=desc)
        unhinted = random.choice(UNHINTED_TEMPLATES).format(desc=desc)

        rows.append({
            "instruction": hinted,
            "output": code,
            "category": f"stdlib/{module}/hinted",
            "task": task,
        })
        rows.append({
            "instruction": unhinted,
            "output": code,
            "category": f"stdlib/{module}/unhinted",
            "task": task,
        })

        # Import-recall variant only if the program actually has imports.
        if imports:
            import_prompt = random.choice(IMPORT_TEMPLATES).format(module=module, desc=desc)
            rows.append({
                "instruction": import_prompt,
                "output": code,
                "category": f"stdlib/{module}/import-recall",
                "task": task,
            })

        per_module[module] = per_module.get(module, 0) + 1

    random.shuffle(rows)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"Generated {len(rows)} Formulary rows -> {OUTPUT_FILE}")
    print(f"Source .hml files: {sum(per_module.values())} across {len(per_module)} modules")
    for m, n in sorted(per_module.items()):
        print(f"  {m:<20} {n}")

    if missing_desc:
        print(f"\nSkipped (no description in formulary_descriptions.py): {len(missing_desc)}")
        for m in missing_desc[:15]:
            print(f"  {m}")

    # Coverage hint: show which of the 53 stdlib modules still need seed tasks.
    all_modules = {
        "arena", "args", "assert", "async", "async_fs", "atomic", "bytes",
        "collections", "compression", "crypto", "csv", "datetime", "debug",
        "decimal", "encoding", "env", "ffi", "fmt", "fs", "glob", "hash",
        "http", "ipc", "iter", "jinja", "json", "logging", "math", "matrix",
        "mmap", "net", "os", "path", "process", "random", "regex", "retry",
        "semver", "shell", "signal", "sqlite", "strings", "terminal", "termios",
        "testing", "time", "toml", "unix_socket", "url", "uuid", "vector",
        "websocket", "yaml",
    }
    uncovered = sorted(all_modules - set(per_module.keys()))
    if uncovered:
        print(f"\nModules with zero seed tasks ({len(uncovered)}/{len(all_modules)}):")
        print("  " + ", ".join(uncovered))


if __name__ == "__main__":
    main()
