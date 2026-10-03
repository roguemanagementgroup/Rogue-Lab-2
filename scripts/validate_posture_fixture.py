"""Validate the repository's intentionally synthetic Windows posture fixture."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

ALLOWED_STATES = {"enabled", "disabled", "unavailable"}
REQUIRED_TOP_LEVEL = {
    "format_version",
    "fixture_kind",
    "asset_reference",
    "collection_mode",
    "os",
    "defender",
    "bitlocker",
    "firewall",
    "updates",
}


def fail(message: str) -> None:
    raise ValueError(message)


def require_exact_keys(name: str, value: object, expected: set[str]) -> dict[str, object]:
    if not isinstance(value, dict):
        fail(f"{name} must be an object")
    actual = set(value)
    if actual != expected:
        fail(f"{name} keys must be {sorted(expected)}, got {sorted(actual)}")
    return value


def require_state(name: str, value: object) -> None:
    if value not in ALLOWED_STATES:
        fail(f"{name} must be one of {sorted(ALLOWED_STATES)}")


def validate_fixture(document: object) -> None:
    root = require_exact_keys("root", document, REQUIRED_TOP_LEVEL)
    if root["format_version"] != "1.0":
        fail("format_version must be '1.0'")
    if root["fixture_kind"] != "synthetic" or root["collection_mode"] != "synthetic-fixture":
        fail("fixture must be explicitly marked synthetic")
    if not isinstance(root["asset_reference"], str) or not re.fullmatch(r"SYNTH-ASSET-\d{3}", root["asset_reference"]):
        fail("asset_reference must be a synthetic opaque reference")

    os_posture = require_exact_keys("os", root["os"], {"product_family", "version", "build"})
    if os_posture["product_family"] != "Windows":
        fail("os.product_family must be 'Windows'")
    if not isinstance(os_posture["version"], str) or not re.fullmatch(r"\d+\.\d+", os_posture["version"]):
        fail("os.version must be a major.minor version")
    if not isinstance(os_posture["build"], str) or not os_posture["build"].isdigit():
        fail("os.build must contain digits only")

    for section, fields in {
        "defender": {"antivirus", "real_time_protection", "service"},
        "firewall": {"domain", "private", "public"},
    }.items():
        values = require_exact_keys(section, root[section], fields)
        for field, value in values.items():
            require_state(f"{section}.{field}", value)

    bitlocker = require_exact_keys(
        "bitlocker", root["bitlocker"], {"system_volume_protection", "protected_volume_count"}
    )
    require_state("bitlocker.system_volume_protection", bitlocker["system_volume_protection"])
    if not isinstance(bitlocker["protected_volume_count"], int) or bitlocker["protected_volume_count"] < 0:
        fail("bitlocker.protected_volume_count must be a non-negative integer")

    updates = require_exact_keys("updates", root["updates"], {"latest_install_date", "currentness"})
    if updates["currentness"] != "not-determined":
        fail("updates.currentness must be 'not-determined'")
    if updates["latest_install_date"] != "unavailable":
        if not isinstance(updates["latest_install_date"], str):
            fail("updates.latest_install_date must be an ISO date or 'unavailable'")
        try:
            date.fromisoformat(updates["latest_install_date"])
        except ValueError as error:
            raise ValueError(
                "updates.latest_install_date must be an ISO date or 'unavailable'"
            ) from error


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "fixture",
        type=Path,
        nargs="?",
        default=Path("fixtures/windows-posture.synthetic.json"),
        help="path to a synthetic posture fixture",
    )
    args = parser.parse_args()
    try:
        document = json.loads(args.fixture.read_text(encoding="utf-8"))
        validate_fixture(document)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"Validation failed: {error}", file=sys.stderr)
        return 1

    print(f"Validated synthetic fixture: {args.fixture}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
