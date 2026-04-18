# Hemlock Apothecary

SFT data for **Hemlock-Apothecary-7B**, a Hemlock-Codex-7B derivative fine-tuned on the **Formulary** — a stdlib-focused dataset that teaches correct imports, API names, and compositions for every `@stdlib/<module>`.

A *formulary* in pharmacology is the reference book listing drug compositions and dosages. Same idea here: one realistic program per (module, task) showing exactly how to compose real stdlib calls.

## Why this exists

`Hemlock-Codex-7B` scored **56.4%** zero-shot on hembench, a generational jump over prior Hemlock fine-tunes. Failure analysis showed its biggest remaining weakness — L2 Stdlib at 40% — came from hallucinated method names (`"hello".capitalize()`) and missing imports (`sqrt(x)` without `import { sqrt } from "@stdlib/math"`). Compact-doc prompting recovered L2 by +20pts but hurt other levels by 14-20pts.

The Formulary is built to hit that failure mode head-on with learned rather than prompted knowledge.

## Structure

```
hemlock/stdlib/<module>/<task>.hml     # one realistic program per (module, task)
formulary_descriptions.py              # (module, task) -> imperative description dict
generate_formulary.py                  # emits hemlock_apothecary_formulary.jsonl
Makefile                               # `make formulary` -> parity check + JSONL
```

Each `.hml` seed becomes up to **3 training rows** with different prompt variants:

| Variant | Prompt form | Teaches |
|---|---|---|
| `hinted` | "Using @stdlib/math, write a Hemlock program to …" | Correct import syntax |
| `unhinted` | "Write a Hemlock program to …" (no module named) | Picking the right module unaided |
| `import-recall` | "What imports do I need from @stdlib/math to …?" | Naming exact symbols |

## Parity-first invariant

Every `.hml` under `hemlock/stdlib/` is verified to produce **byte-identical output** under both the tree-walking interpreter (`./hemlock`) and the C-compiled binary (`./hemlockc`). `make check-seeds` enforces this on every run of `make formulary`, so a seed that diverges cannot silently enter training data.

This constraint has already surfaced seven real parity bugs in `hemlang/hemlock` (PRs #519, #520, #521, #522, #526, #527 plus d6b2587); see that repo's history for details.

## Usage

```bash
# Build hemlock + hemlockc in the main repo first
(cd ~/Projects/hemlock && make all)

# Generate (runs parity check then writes JSONL)
make formulary

# Combine with hemlock-codex for a full training set
cat ~/Projects/hemlock-codex/hemlock_codex_sft.jsonl \
    hemlock_apothecary_formulary.jsonl \
    > apothecary_training.jsonl
```

## Schema

Matches `hemlock-codex`'s output schema so the two concatenate directly:

```json
{
  "instruction": "Using @stdlib/math, write a Hemlock program to ...",
  "output":      "import { sqrt } from \"@stdlib/math\";\n\n...",
  "category":    "stdlib/math/hinted",
  "task":        "sqrt_distance"
}
```

The `category` prefix lets you filter/weight rows by source (`translation/*`, `generation/*`, `stdlib/*`) during training.

## Current coverage

83 seeds across 28 of 53 stdlib modules → **249 training rows**. Remaining 25 modules are mostly I/O or nondeterministic output (time, logging, http, net, fs, process, signal, …) — doable but require sandboxing to keep seed output reproducible.

Priority fill order for future seeds is tracked at the bottom of `formulary_descriptions.py`.
