"""Print deterministic subproblem variants of one decimal-arithmetic prompt."""

from __future__ import annotations

import argparse
import random
from pathlib import Path

from decimal_subproblem_augmentation import DecimalSubproblemAugmenter


DEFAULT_QUESTION = (
    "Please solve this problem to a maximum of 12 significant digits.\n"
    "(6.5300-3.06)*2.50 = ?"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--question", default=DEFAULT_QUESTION)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--count", type=int, default=3)
    parser.add_argument("--wording-bank", type=Path)
    parser.add_argument("--two-step-probability", type=float, default=0.25)
    parser.add_argument("--two-subproblem-probability", type=float, default=0.15)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = {
        "two_step_probability": args.two_step_probability,
        "two_subproblem_probability": args.two_subproblem_probability,
    }
    if args.wording_bank:
        config.update(
            {
                "renderer_source": "mixed",
                "renderer_bank_path": str(args.wording_bank),
                "offline_probability": 0.5,
            }
        )
    augmenter = DecimalSubproblemAugmenter(config, random.Random(args.seed))
    for index in range(args.count):
        print(f"--- Variant {index + 1} ---")
        print(augmenter.augment(args.question, task_name="decimal_arithmetic"))


if __name__ == "__main__":
    main()

