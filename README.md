# Decimal Subproblem Augmentation

This repository contains the standalone subproblem-augmentation component used in
*Augment, Prioritise, Learn*. It transforms a direct decimal-arithmetic prompt into
an exactly equivalent composed problem: one or two operands are represented by
variables whose values must first be recovered from auxiliary mathematical clues.

The transformation is deterministic under a fixed random seed and does not require
a language model, network connection, or learned verifier at runtime. Auxiliary
problems are constructed backwards from the original operands, allowing the original
answer and verifier target to remain unchanged.

## What is included

- 15 exact mathematical construction families;
- three built-in phrasings per family and six prompt layouts;
- optional two-step recovery and two-operand composition;
- support for built-in, reviewed offline, or mixed wording sources;
- the reviewed Qwen3-14B wording bank used in the study;
- a small command-line example; and
- integration guidance for Accel-verl.

## Installation

```bash
python -m pip install -e .
```

## Usage

```python
import random

from decimal_subproblem_augmentation import DecimalSubproblemAugmenter

question = (
    "Please solve this problem to a maximum of 12 significant digits.\n"
    "(6.5300-3.06)*2.50 = ?"
)

augmenter = DecimalSubproblemAugmenter(
    {
        "two_step_probability": 0.25,
        "two_subproblem_probability": 0.15,
        "renderer_source": "builtin",
    },
    random.Random(42),
)

print(augmenter.augment(question, task_name="decimal_arithmetic"))
```

To use the reviewed offline wording bank:

```python
augmenter = DecimalSubproblemAugmenter(
    {
        "renderer_source": "mixed",
        "renderer_bank_path": "data/decimal_subproblem_wordings.json",
        "offline_probability": 0.5,
    },
    random.Random(42),
)
```

Run `python examples/augment_prompt.py --help` for a complete executable example.

## Accel-verl integration

The core package has no dependency on veRL or Accel-verl. The files under
`integration/` document the small adapter used to call the augmenter from the
training pipeline and the separate intervention that prevents augmented rewards
from updating curriculum-regret estimates.

The integration notes target the Rhine AI Lab Accel-verl codebase at the upstream
revision recorded in `integration/UPSTREAM.md`. They are not required to use the
standalone package.

## Offline wording

The checked-in wording bank contains only variants that passed structural checks and
manual review. The review report records which teacher-generated families were
accepted and which were rejected. Offline wording affects presentation only; all
underlying numerical relationships are still created and checked by the deterministic
augmentation code.

## Attribution

The training integration used in the dissertation targeted the
[Rhine-AI-Lab/Accel-verl](https://github.com/Rhine-AI-Lab/Accel-verl) codebase. This
repository does not vendor Accel-verl or veRL. See `integration/UPSTREAM.md` for the
recorded upstream revision.
