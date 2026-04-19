---
license: mit
task_categories:
- text-generation
language:
- en
tags:
- code
- hemlock
- sft
- fine-tuning
- stdlib
- code-generation
pretty_name: Hemlock Apothecary Formulary
size_categories:
- n<1K
configs:
- config_name: default
  data_files:
  - split: train
    path: hemlock_apothecary_formulary.jsonl
---

# Hemlock Apothecary Formulary

Stdlib-focused SFT data for fine-tuning Hemlock-Apothecary-7B — a
[Hemlock-Codex-7B](https://huggingface.co/hemlang/Hemlock-Codex-7B) derivative
aimed at closing the L2-Stdlib gap measured on [hembench](https://github.com/hemlang/hemlock/tree/main/benchmark).

A *formulary* in pharmacology is the reference book listing drug compositions and dosages.
Same idea here: one realistic program per `(@stdlib/<module>, task)` pair showing
exactly how to compose real Hemlock stdlib calls — right imports, right method names,
right idioms.

## Why this dataset exists

Evaluating `Hemlock-Codex-7B` at Q8_0 zero-shot on hembench surfaced a distinctive
failure mode on L2 (Stdlib): **hallucinated method names and missing imports**.
Typical misses:

- `"hello".capitalize()` — no such method on Hemlock strings
- `sqrt(x)` without `import { sqrt } from "@stdlib/math";`
- `atomic_load_i32` called but never imported
- `obj.iter()` — a Pythonism, not a Hemlock API

Compact-doc prompting recovered L2 but hurt other levels by 14–20pts (docs in-prompt
pull the fine-tune away from its learned idioms). The Formulary attacks the failure
mode through training rather than prompting.

## Dataset structure

Each row is a single instruction/output SFT pair:

```json
{
  "instruction": "Using @stdlib/math, write a Hemlock program to compute 2D Euclidean distance for a few point pairs and print each result to 4 decimal places.",
  "output":      "import { sqrt, pow } from \"@stdlib/math\";\nimport { to_fixed } from \"@stdlib/decimal\";\n\nfn distance(x1: f64, y1: f64, x2: f64, y2: f64): f64 {\n    ...\n}\n\n...",
  "category":    "stdlib/math/hinted",
  "task":        "sqrt_distance"
}
```

### Fields

| Field | Type | Description |
|---|---|---|
| `instruction` | string | Natural-language task prompt |
| `output` | string | Complete, runnable Hemlock program |
| `category` | string | `stdlib/<module>/<variant>` — useful for filtering or weighting at train time |
| `task` | string | Short slug identifying the source seed |

### Prompt variants

Each of the 83 source seeds is expanded into up to **3 rows** so the model learns both
correct imports *and* module recognition:

| Variant | Prompt form | Teaches |
|---|---|---|
| `hinted` | "Using @stdlib/math, write …" | Exact import syntax when the module is known |
| `unhinted` | "Write a Hemlock program to …" | Picking the right module from the problem description |
| `import-recall` | "What imports do I need from @stdlib/math to …?" | Naming exact symbols |

## Composition

**249 rows across 83 seed programs covering 28 of Hemlock's 53 stdlib modules.**

| Module | Seeds | Module | Seeds | Module | Seeds |
|---|---|---|---|---|---|
| math | 8 | datetime | 4 | args | 1 |
| json | 6 | encoding | 3 | assert | 1 |
| collections | 6 | fmt | 3 | async | 1 |
| decimal | 5 | iter | 3 | hash | 1 |
| strings | 5 | matrix | 3 | testing | 1 |
| csv | 4 | path | 3 | | |
| | | url | 3 | | |
| | | atomic | 2 | | |
| | | bytes | 2 | | |
| | | compression | 2 | | |
| | | random | 2 | | |
| | | regex | 2 | | |
| | | semver | 2 | | |
| | | toml | 2 | | |
| | | uuid | 2 | | |
| | | yaml | 2 | | |

The remaining 25 modules are mostly I/O or nondeterministic (`time`, `logging`,
`http`, `net`, `fs`, `process`, etc.) — reachable but require sandboxing to keep
seed output reproducible. PRs welcome.

## Methodology: parity-first

Every seed program under `hemlock/stdlib/**/*.hml` is verified to produce
**byte-identical output** under both Hemlock execution backends:

1. `./hemlock` — the tree-walking interpreter
2. `./hemlockc` — the C code generator, linked against libhemlock_runtime

Divergent programs never enter training data. This constraint is enforced by
`make check-seeds` in the source repo and runs on every regeneration.

Applying it surfaced **7 real compiler/interpreter parity bugs** in the Hemlock
runtime that have since been fixed:

- LinkedList iteration miscompile (PR #519)
- `regex.replace_all` segfault under compiler (PR #520)
- `path.normalize` on `../..` (PR #521)
- toml array element unboxing (d6b2587)
- `for (x in array)` + stdlib-call type confusion (PR #522)
- `LinkedList.reverse()` routing to array path (PR #526)
- Generalized array-method dispatch on object receivers (PR #527)

## Intended use

**Recommended:** continued SFT on top of
[Hemlock-Codex-7B](https://huggingface.co/hemlang/Hemlock-Codex-7B),
mixed with a small replay sample (~20%) from Codex's original SFT to prevent
catastrophic forgetting on L3/L5.

```python
from datasets import load_dataset

formulary = load_dataset("hemlang/hemlock-apothecary", split="train")
print(len(formulary))  # 249
print(formulary[0])
```

Concatenate with Codex's SFT for a combined training run:

```python
from datasets import concatenate_datasets, load_dataset

codex     = load_dataset("hemlang/hemlock-codex",      split="train")  # 552 rows
formulary = load_dataset("hemlang/hemlock-apothecary", split="train")  # 249 rows
combined  = concatenate_datasets([codex, formulary])                   # 801 rows
```

Filter by category to rebalance the mix at train time:

```python
stdlib_only = formulary.filter(lambda r: r["category"].startswith("stdlib/"))
imports_only = formulary.filter(lambda r: r["category"].endswith("/import-recall"))
```

## Limitations

- **Small.** 83 unique programs is limited coverage; 3× variant expansion is a
  training-efficiency trick, not a breadth increase.
- **Deterministic-output bias.** Modules with nondeterministic output (time,
  logging, random without seed, network, process) are excluded. Models trained
  on this dataset alone will be weakest on those modules.
- **English-only prompts.** The Codex base was trained with multilingual data;
  this dataset is English.
- **Hemlock-specific.** Useless for anything other than Hemlock-family fine-tunes.

## Source repo

Full seed sources, generator, parity-check Makefile, and regen pipeline:
[hemlang/hemlock-apothecary](https://github.com/hemlang/hemlock-apothecary) on GitHub.

## Citation

```bibtex
@misc{hemlock_apothecary_formulary_2026,
  title   = {Hemlock Apothecary Formulary: Stdlib-Focused SFT for Hemlock Fine-Tunes},
  author  = {Hemlock Language Project},
  year    = {2026},
  url     = {https://huggingface.co/datasets/hemlang/hemlock-apothecary}
}
```

## License

MIT (matches the Hemlock language repo).
