"""Exact, teacher-free subproblem augmentation for decimal arithmetic."""

from .augmenter import (
    DecimalSubproblemAugmenter,
    template_fields,
    validate_renderer_bank,
)

__all__ = [
    "DecimalSubproblemAugmenter",
    "template_fields",
    "validate_renderer_bank",
]

