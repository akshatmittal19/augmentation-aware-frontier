"""Verified, teacher-free subproblem augmentation for decimal arithmetic."""

import ast
import json
import random
import re
from decimal import Decimal, InvalidOperation, localcontext
from pathlib import Path
from string import Formatter
from typing import Any, Callable, Dict, List, Optional, Tuple

from .templates import (
    BUILTIN_FAMILY_TEMPLATES,
    FAMILY_FIELDS,
    FAMILY_GROUPS,
    INTEGRATION_TEMPLATES,
    TRANSITION_TEMPLATES,
)

FamilyResult = Tuple[str, Decimal, Dict[str, str]]

_QUESTION_RE = re.compile(
    r"^(?P<prefix>.*\n)?(?P<expression>[^\n]+?)\s*=\s*\?\s*$", re.DOTALL
)
_NUMBER_RE = re.compile(r"(?<![\w.])(?:\d+\.\d+|\d+)(?![\w.])")


def template_fields(template: str) -> set:
    """Return simple format placeholders, rejecting attributes and format specs."""
    fields = set()
    for _literal, name, format_spec, conversion in Formatter().parse(template):
        if name is None:
            continue
        if not re.fullmatch(r"[a-z_]+", name) or format_spec or conversion:
            raise ValueError(f"Unsafe placeholder in renderer template: {name!r}")
        fields.add(name)
    return fields


def validate_renderer_bank(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Validate an offline teacher bank before it can affect training prompts."""
    if int(payload.get("version", 0)) != 1:
        raise ValueError("Renderer bank must have version 1")
    validated = {"version": 1, "families": {}, "integration_templates": []}
    raw_families = payload.get("families", {})
    if not isinstance(raw_families, dict):
        raise ValueError("Renderer bank 'families' must be a mapping")
    for family, templates in raw_families.items():
        if family not in FAMILY_FIELDS or not isinstance(templates, list):
            continue
        accepted = []
        for template in templates:
            if (
                isinstance(template, str)
                and template.strip()
                and template_fields(template) == FAMILY_FIELDS[family]
            ):
                accepted.append(template.strip())
        if accepted:
            validated["families"][family] = list(dict.fromkeys(accepted))
    for template in payload.get("integration_templates", []):
        if (
            isinstance(template, str)
            and template.strip()
            and template_fields(template) == {"clues", "expression"}
        ):
            validated["integration_templates"].append(template.strip())
    return validated


def _plain(value: Decimal) -> str:
    rendered = format(value, "f")
    if "." in rendered:
        rendered = rendered.rstrip("0").rstrip(".")
    return rendered or "0"


def _is_decimal_expression(expression: str) -> bool:
    """Accept only the arithmetic grammar emitted by decimal_arithmetic."""
    try:
        tree = ast.parse(expression, mode="eval")
    except (SyntaxError, ValueError):
        return False
    binary_ops = (ast.Add, ast.Sub, ast.Mult, ast.Div)
    unary_ops = (ast.UAdd, ast.USub)
    structural = (ast.Expression, ast.BinOp, ast.UnaryOp)
    for node in ast.walk(tree):
        if isinstance(node, ast.BinOp) and not isinstance(node.op, binary_ops):
            return False
        if isinstance(node, ast.UnaryOp) and not isinstance(node.op, unary_ops):
            return False
        if isinstance(node, ast.Constant):
            if isinstance(node.value, bool) or not isinstance(node.value, (int, float)):
                return False
        elif not isinstance(node, structural + binary_ops + unary_ops):
            return False
    return True


class DecimalSubproblemAugmenter:
    """Replace one operand with a variable recovered by an exact subproblem."""

    DEFAULT_VARIABLES = ["x", "y", "d", "q", "r"]

    def __init__(self, cfg: Optional[Dict[str, Any]], rng: random.Random):
        self.cfg = cfg or {}
        self._rng = rng
        self.two_step_probability = float(self.cfg.get("two_step_probability", 0.25))
        self.two_subproblem_probability = float(
            self.cfg.get("two_subproblem_probability", 0.15)
        )
        self.renderer_source = str(
            self.cfg.get("renderer_source", "builtin")
        ).strip().lower()
        self.offline_probability = float(self.cfg.get("offline_probability", 0.5))
        self.task_names = {
            str(name).strip().lower()
            for name in self.cfg.get(
                "task_names", ["decimal_arithmetic", "decimal_arithmnetic"]
            )
        }
        variables = self.cfg.get("variables", self.DEFAULT_VARIABLES)
        self.variables = [
            str(name).strip()
            for name in variables
            if re.fullmatch(r"[A-Za-z]", str(name).strip())
        ] or list(self.DEFAULT_VARIABLES)
        self._families: Dict[
            str, Callable[[Decimal, str], FamilyResult]
        ] = {
            "additive_balance": self._additive_balance,
            "subtraction_remainder": self._subtraction_remainder,
            "equal_shares": self._equal_shares,
            "unit_price": self._unit_price,
            "rectangle_area": self._rectangle_area,
            "rectangle_perimeter": self._rectangle_perimeter,
            "constant_rate": self._constant_rate,
            "missing_average": self._missing_average,
            "midpoint": self._midpoint,
            "map_scale": self._map_scale,
            "arithmetic_sequence": self._arithmetic_sequence,
            "equal_edge_path": self._equal_edge_path,
            "percentage": self._percentage,
            "place_value": self._place_value,
            "quotient": self._quotient,
        }
        configured = self.cfg.get("families")
        if configured is None:
            self.family_names = list(self._families)
        else:
            self.family_names = [
                str(name).strip()
                for name in configured
                if str(name).strip() in self._families
            ]

        self.offline_bank = {"families": {}, "integration_templates": []}
        bank_path = str(self.cfg.get("renderer_bank_path", "")).strip()
        if bank_path:
            with Path(bank_path).expanduser().open(encoding="utf-8") as handle:
                raw_bank = json.load(handle)
            review_status = str(
                raw_bank.get("generator", {}).get("review_status", "")
            ).strip()
            if (
                review_status == "candidate_requires_human_review"
                and not bool(self.cfg.get("allow_unreviewed_renderer_bank", False))
            ):
                raise ValueError("Offline renderer bank still requires human review")
            self.offline_bank = validate_renderer_bank(raw_bank)
        if self.renderer_source not in {"builtin", "offline", "mixed"}:
            raise ValueError(
                "subproblem.renderer_source must be builtin, offline, or mixed"
            )
        if self.renderer_source == "offline":
            missing = set(self.family_names) - set(self.offline_bank["families"])
            if missing or not self.offline_bank["integration_templates"]:
                raise ValueError(
                    "renderer_source=offline requires every selected family and an "
                    f"integration template; missing={sorted(missing)}"
                )

    @property
    def available_families(self) -> List[str]:
        return list(self._families)

    def _choose_family(self) -> str:
        available = set(self.family_names)
        groups = [
            [family for family in members if family in available]
            for members in FAMILY_GROUPS.values()
        ]
        groups = [group for group in groups if group]
        return self._rng.choice(self._rng.choice(groups))

    def _use_offline(self, family: str) -> bool:
        has_family = bool(self.offline_bank["families"].get(family))
        if self.renderer_source == "offline":
            return has_family
        if self.renderer_source == "mixed":
            return has_family and self._rng.random() < self.offline_probability
        return False

    def _render_clue(
        self, family: str, canonical: str, values: Dict[str, str]
    ) -> str:
        if self._use_offline(family):
            templates = self.offline_bank["families"][family]
        else:
            templates = BUILTIN_FAMILY_TEMPLATES.get(family, [])
        if not templates:
            return canonical
        return self._rng.choice(templates).format(**values)

    def _integration_templates(self) -> List[str]:
        if self.renderer_source == "offline":
            return self.offline_bank["integration_templates"] or INTEGRATION_TEMPLATES
        if self.renderer_source == "mixed" and self.offline_bank["integration_templates"]:
            if self._rng.random() < self.offline_probability:
                return self.offline_bank["integration_templates"]
        return INTEGRATION_TEMPLATES

    def augment(self, question: str, task_name: str) -> str:
        if task_name.strip().lower() not in self.task_names or not self.family_names:
            return question
        match = _QUESTION_RE.fullmatch(question.strip())
        if match is None:
            return question
        expression = match.group("expression").strip()
        if not _is_decimal_expression(expression):
            return question
        operands = list(_NUMBER_RE.finditer(expression))
        if not operands:
            return question

        count = 1
        if (
            len(operands) > 1
            and len(self.variables) > 1
            and self._rng.random() < self.two_subproblem_probability
        ):
            count = 2
        selected = sorted(self._rng.sample(operands, count), key=lambda item: item.start())
        variables = self._rng.sample(self.variables, count)
        replacements = []
        clues = []
        used_variables = set(variables)
        for index, (operand, variable) in enumerate(zip(selected, variables), start=1):
            try:
                target = Decimal(operand.group(0))
            except InvalidOperation:
                return question
            if not target.is_finite() or target <= 0:
                return question

            family = self._choose_family()
            two_step = self._rng.random() < self.two_step_probability
            family_target = target
            family_variable = variable
            offset = None
            if two_step:
                offset = self._small_int()
                family_target = target + offset
                candidates = [
                    name
                    for name in self.DEFAULT_VARIABLES
                    if name not in used_variables
                ]
                if candidates:
                    family_variable = self._rng.choice(candidates)
                    used_variables.add(family_variable)
                else:
                    two_step = False
                    family_target = target
                    offset = None

            try:
                with localcontext() as ctx:
                    ctx.prec = max(64, len(family_target.as_tuple().digits) + 32)
                    canonical, recovered, values = self._families[family](
                        family_target, family_variable
                    )
            except (ArithmeticError, InvalidOperation, ValueError):
                return question
            if recovered != family_target:
                return question

            clue = self._render_clue(family, canonical, values)
            if two_step and offset is not None:
                transition = self._rng.choice(TRANSITION_TEMPLATES).format(
                    output_variable=variable,
                    intermediate_variable=family_variable,
                    offset=_plain(offset),
                )
                clue = f"{clue} {transition}"
                if recovered - offset != target:
                    return question
            label = f"Subproblem {index}: " if count > 1 else ""
            clues.append(f"{label}{clue}")
            replacements.append((operand.start(), operand.end(), variable))

        transformed = expression
        for start, end, variable in reversed(replacements):
            transformed = transformed[:start] + variable + transformed[end:]
        prefix = (match.group("prefix") or "").rstrip()
        augmented = self._rng.choice(self._integration_templates()).format(
            clues="\n".join(clues),
            expression=transformed,
        )
        return f"{prefix}\n{augmented}" if prefix else augmented

    def _small_int(self, low: int = 2, high: int = 9) -> Decimal:
        return Decimal(self._rng.randint(low, high))

    def _additive_balance(self, t: Decimal, v: str) -> FamilyResult:
        k = self._small_int()
        total = t + k
        return (
            f"Two containers hold {_plain(total)} liters altogether. One holds "
            f"{_plain(k)} liters. How many liters, denoted by {v}, does the other hold?",
            total - k,
            {"total": _plain(total), "known": _plain(k), "variable": v},
        )

    def _subtraction_remainder(self, t: Decimal, v: str) -> FamilyResult:
        k = self._small_int()
        initial = t + k
        return (
            f"A tank initially contains {_plain(initial)} liters. After {_plain(k)} "
            f"liters are removed, its remaining volume is {v} liters. Find {v}.",
            initial - k,
            {"initial": _plain(initial), "removed": _plain(k), "variable": v},
        )

    def _equal_shares(self, t: Decimal, v: str) -> FamilyResult:
        n = self._small_int()
        total = t * n
        return (
            f"{_plain(total)} kilograms are divided equally among {int(n)} boxes. "
            f"If each box receives {v} kilograms, find {v}.",
            total / n,
            {"total": _plain(total), "count": str(int(n)), "variable": v},
        )

    def _unit_price(self, t: Decimal, v: str) -> FamilyResult:
        n = self._small_int()
        total = t * n
        return (
            f"{int(n)} identical notebooks cost {_plain(total)} units in total. "
            f"Their common unit price is {v}. Find {v}.",
            total / n,
            {"count": str(int(n)), "total": _plain(total), "variable": v},
        )

    def _rectangle_area(self, t: Decimal, v: str) -> FamilyResult:
        width = self._small_int()
        area = t * width
        return (
            f"A rectangle has area {_plain(area)} square units and width {_plain(width)} "
            f"units. Its length is {v} units. Find {v}.",
            area / width,
            {"area": _plain(area), "width": _plain(width), "variable": v},
        )

    def _rectangle_perimeter(self, t: Decimal, v: str) -> FamilyResult:
        width = self._small_int()
        perimeter = Decimal(2) * (t + width)
        return (
            f"A rectangle has perimeter {_plain(perimeter)} units and width "
            f"{_plain(width)} units. Its length is {v} units. Find {v}.",
            perimeter / Decimal(2) - width,
            {
                "perimeter": _plain(perimeter),
                "width": _plain(width),
                "variable": v,
            },
        )

    def _constant_rate(self, t: Decimal, v: str) -> FamilyResult:
        hours = self._small_int()
        distance = t * hours
        return (
            f"An object travels {_plain(distance)} kilometers in {int(hours)} hours "
            f"at a constant rate of {v} kilometers per hour. Find {v}.",
            distance / hours,
            {
                "distance": _plain(distance),
                "hours": str(int(hours)),
                "variable": v,
            },
        )

    def _missing_average(self, t: Decimal, v: str) -> FamilyResult:
        known = self._small_int()
        mean = (t + known) / Decimal(2)
        return (
            f"The arithmetic mean of {_plain(known)} and {v} is {_plain(mean)}. Find {v}.",
            Decimal(2) * mean - known,
            {"known": _plain(known), "mean": _plain(mean), "variable": v},
        )

    def _midpoint(self, t: Decimal, v: str) -> FamilyResult:
        endpoint = self._small_int()
        midpoint = (t + endpoint) / Decimal(2)
        return (
            f"On a number line, the midpoint of {_plain(endpoint)} and {v} is "
            f"{_plain(midpoint)}. Find {v}.",
            Decimal(2) * midpoint - endpoint,
            {
                "endpoint": _plain(endpoint),
                "midpoint": _plain(midpoint),
                "variable": v,
            },
        )

    def _map_scale(self, t: Decimal, v: str) -> FamilyResult:
        scale = self._small_int()
        actual = t * scale
        return (
            f"A map uses a 1:{int(scale)} scale. A segment represents {_plain(actual)} "
            f"centimeters in reality and measures {v} centimeters on the map. Find {v}.",
            actual / scale,
            {
                "scale": str(int(scale)),
                "actual": _plain(actual),
                "variable": v,
            },
        )

    def _arithmetic_sequence(self, t: Decimal, v: str) -> FamilyResult:
        first = self._small_int()
        steps = self._small_int(2, 6)
        last = first + steps * t
        return (
            f"An arithmetic sequence starts at {_plain(first)} and term number {int(steps) + 1} "
            f"is {_plain(last)}. Its common difference is {v}. Find {v}.",
            (last - first) / steps,
            {
                "first": _plain(first),
                "index": str(int(steps) + 1),
                "last": _plain(last),
                "variable": v,
            },
        )

    def _equal_edge_path(self, t: Decimal, v: str) -> FamilyResult:
        edges = self._small_int()
        total = t * edges
        return (
            f"A path consists of {int(edges)} edges of equal weight and has total "
            f"weight {_plain(total)}. Each edge has weight {v}. Find {v}.",
            total / edges,
            {"edges": str(int(edges)), "total": _plain(total), "variable": v},
        )

    def _percentage(self, t: Decimal, v: str) -> FamilyResult:
        percent = Decimal(self._rng.choice([10, 20, 25, 50]))
        total = t * Decimal(100) / percent
        return (
            f"A quantity {v} is {int(percent)} percent of {_plain(total)}. Find {v}.",
            total * percent / Decimal(100),
            {
                "percent": str(int(percent)),
                "total": _plain(total),
                "variable": v,
            },
        )

    def _place_value(self, t: Decimal, v: str) -> FamilyResult:
        places = max(1, -t.as_tuple().exponent)
        scale = Decimal(10) ** places
        integer = t * scale
        return (
            f"Dividing the integer {_plain(integer)} by 10^{places} gives {v}. Find {v}.",
            integer / scale,
            {
                "integer": _plain(integer),
                "places": str(places),
                "variable": v,
            },
        )

    def _quotient(self, t: Decimal, v: str) -> FamilyResult:
        denominator = self._small_int()
        numerator = t * denominator
        return (
            f"The quotient of {_plain(numerator)} divided by {_plain(denominator)} "
            f"is {v}. Find {v}.",
            numerator / denominator,
            {
                "numerator": _plain(numerator),
                "denominator": _plain(denominator),
                "variable": v,
            },
        )
