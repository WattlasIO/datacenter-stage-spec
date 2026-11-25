#!/usr/bin/env python3
"""Zero-dependency validator for Pre-Operational Data Center Project Records."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
from pathlib import Path
from typing import Any

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
STATE_RE = re.compile(r"^[A-Z]{2}$")

STAGE_QUALIFYING_RECORDS: dict[str, set[str]] = {
    "announced": {
        "press_release",
        "incentive_agreement",
        "zoning_application",
        "zoning_approval",
        "site_plan_permit",
        "environmental_permit",
        "utility_filing",
        "building_permit",
        "construction_notice",
        "energization_notice",
    },
    "zoning_filed": {
        "zoning_application",
        "zoning_approval",
        "site_plan_permit",
        "environmental_permit",
        "building_permit",
        "construction_notice",
        "energization_notice",
    },
    "zoning_approved": {
        "zoning_approval",
        "site_plan_permit",
        "environmental_permit",
        "building_permit",
        "construction_notice",
        "energization_notice",
    },
    "site_permit": {
        "site_plan_permit",
        "environmental_permit",
        "utility_filing",
        "building_permit",
        "construction_notice",
        "energization_notice",
    },
    "building_permit": {
        "building_permit",
        "construction_notice",
        "energization_notice",
    },
    "under_construction": {
        "construction_notice",
        "energization_notice",
    },
    "energized": {
        "energization_notice",
    },
}

CAPACITY_BASES = {
    "it_load_mw",
    "utility_load_mw",
    "interconnection_request_mw",
    "generation_nameplate_mw",
    "undisclosed",
}


def validate_record(rec: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    name = rec.get("project_name")
    if not isinstance(name, str) or len(name.strip()) < 2:
        errors.append("project_name must be a non-empty string (min length 2).")

    state = rec.get("state")
    if not isinstance(state, str) or not STATE_RE.match(state):
        errors.append("state must be a 2-letter uppercase US postal code.")

    obs = rec.get("observed_date")
    if not isinstance(obs, str) or not DATE_RE.match(obs):
        errors.append("observed_date must match YYYY-MM-DD.")

    stage = rec.get("stage")
    if not isinstance(stage, str) or stage not in STAGE_QUALIFYING_RECORDS:
        errors.append(f"Invalid stage '{stage}'.")

    cap = rec.get("capacity")
    if cap is not None:
        if not isinstance(cap, dict):
            errors.append("capacity must be an object.")
        else:
            basis = cap.get("basis")
            mw = cap.get("mw")
            if basis not in CAPACITY_BASES:
                errors.append(f"Invalid capacity.basis '{basis}'.")
            if basis == "undisclosed" and mw is not None:
                errors.append("capacity.mw must be null when capacity.basis is 'undisclosed'.")
            if basis in CAPACITY_BASES - {"undisclosed"}:
                if not isinstance(mw, (int, float)) or isinstance(mw, bool) or mw <= 0:
                    errors.append("capacity.mw must be a positive number when capacity.basis is disclosed.")

    evidence = rec.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        errors.append("evidence must be a non-empty list of source records.")
        return errors

    record_types: set[str] = set()
    for idx, ev in enumerate(evidence):
        if not isinstance(ev, dict):
            errors.append(f"evidence[{idx}] must be an object.")
            continue
        rtype = ev.get("record_type")
        if isinstance(rtype, str):
            record_types.add(rtype)
        else:
            errors.append(f"evidence[{idx}].record_type is required.")

        url = ev.get("url")
        if not isinstance(url, str):
            errors.append(f"evidence[{idx}].url must be an https:// URL.")
        else:
            parsed = urllib.parse.urlparse(url)
            if parsed.scheme != "https" or not parsed.netloc:
                errors.append(f"evidence[{idx}].url must be a valid https:// URL.")

        fdate = ev.get("filed_date")
        if not isinstance(fdate, str) or not DATE_RE.match(fdate):
            errors.append(f"evidence[{idx}].filed_date must match YYYY-MM-DD.")

        summary = ev.get("summary")
        if not isinstance(summary, str) or len(summary.strip()) < 5:
            errors.append(f"evidence[{idx}].summary must be at least 5 characters.")

    if isinstance(stage, str) and stage in STAGE_QUALIFYING_RECORDS:
        allowed = STAGE_QUALIFYING_RECORDS[stage]
        if not (record_types & allowed):
            errors.append(
                f"Stage '{stage}' is not supported by evidence record_types {sorted(record_types)}; "
                f"requires at least one of {sorted(allowed)}."
            )

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate pre-operational data center project records.")
    parser.add_argument("files", nargs="+", type=Path, help="JSON file(s) containing a record object or list.")
    args = parser.parse_args(argv)

    failed = False
    for path in args.files:
        raw = json.loads(path.read_text(encoding="utf-8"))
        records = raw if isinstance(raw, list) else [raw]
        for idx, rec in enumerate(records):
            errs = validate_record(rec)
            if errs:
                failed = True
                print(f"[FAIL] {path} #{idx}:")
                for err in errs:
                    print(f"  - {err}")
            else:
                print(f"[PASS] {path} #{idx}: {rec['project_name']} ({rec['stage']})")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
