#!/usr/bin/env python3
"""Preflight text fit risks in a reconstruction plan before PPTX packaging."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ORPHAN_PUNCTUATION = set("，。！？；：、,.!?;:")


def as_bool(value: Any, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    normalized = str(value).strip().lower()
    if normalized in {"1", "true", "yes", "y", "on"}:
        return True
    if normalized in {"0", "false", "no", "n", "off"}:
        return False
    return default


def load_plan(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def text_elements(plan: dict[str, Any]) -> list[dict[str, Any]]:
    elements: list[dict[str, Any]] = []
    for slide_index, slide in enumerate(plan.get("slides", []), start=1):
        for element_index, element in enumerate(slide.get("elements", []), start=1):
            if element.get("type") == "text":
                copy = dict(element)
                copy["_slide_index"] = slide_index
                copy["_element_index"] = element_index
                elements.append(copy)
    return elements


def text_lines(element: dict[str, Any]) -> list[str]:
    return str(element.get("text", "")).splitlines() or [""]


def line_width_inches(line: str, font_size: float) -> float:
    width_units = sum(1.0 if ord(ch) > 127 else 0.55 for ch in line)
    return width_units * font_size * 0.58 / 72.0


def fit_reasons(element: dict[str, Any]) -> list[str]:
    font_size = float(element.get("font_size", 14))
    margin = float(element.get("margin", 0.03))
    box_w = max(float(element.get("w", 0)) - margin * 2, 0.01)
    box_h = max(float(element.get("h", 0)) - margin * 2, 0.01)
    lines = text_lines(element)
    needed_h = len(lines) * font_size * 1.18 / 72.0
    reasons: list[str] = []
    if needed_h > box_h:
        reasons.append("height")

    word_wrap = as_bool(element.get("word_wrap"), True)
    if as_bool(element.get("no_wrap"), False):
        word_wrap = False
    if not word_wrap:
        max_needed_w = max((line_width_inches(line, font_size) for line in lines), default=0.0)
        if max_needed_w > box_w:
            reasons.append("width_no_wrap")
    return reasons


def check_element(element: dict[str, Any]) -> list[dict[str, Any]]:
    warnings: list[dict[str, Any]] = []
    element_id = str(element.get("id", f"text-{element.get('_slide_index')}-{element.get('_element_index')}"))
    reasons = fit_reasons(element)
    if reasons:
        warnings.append(
            {
                "id": element_id,
                "warning": "text_overflow_risk",
                "reasons": reasons,
                "text_preview": str(element.get("text", ""))[:80],
            }
        )

    for line_no, line in enumerate(text_lines(element), start=1):
        stripped = line.strip()
        if stripped and stripped[0] in ORPHAN_PUNCTUATION:
            warnings.append(
                {
                    "id": element_id,
                    "warning": "punctuation_orphan_line",
                    "line": line_no,
                    "text_preview": stripped[:20],
                }
            )
        elif len(stripped) == 1 and ord(stripped) > 127:
            warnings.append(
                {
                    "id": element_id,
                    "warning": "single_character_line",
                    "line": line_no,
                    "text_preview": stripped,
                }
            )
    return warnings


def check_plan(plan: dict[str, Any]) -> dict[str, Any]:
    elements = text_elements(plan)
    warnings: list[dict[str, Any]] = []
    for element in elements:
        warnings.extend(check_element(element))
    by_type: dict[str, int] = {}
    for warning in warnings:
        by_type[warning["warning"]] = by_type.get(warning["warning"], 0) + 1
    return {
        "tool": "check_reconstruction_plan_text_fit.py",
        "status": "warnings" if warnings else "pass",
        "summary": {
            "text_elements": len(elements),
            "warning_count": len(warnings),
            "warnings_by_type": by_type,
        },
        "warnings": warnings,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Check reconstruction plan text fit risks.")
    parser.add_argument("plan", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    report = check_plan(load_plan(args.plan))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], **report["summary"]}, ensure_ascii=False))
    raise SystemExit(0 if report["status"] == "pass" else 2)


if __name__ == "__main__":
    main()
