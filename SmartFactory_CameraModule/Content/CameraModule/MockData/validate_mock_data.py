import json
import re
import argparse
import sys
from datetime import datetime
from pathlib import Path


EXPECTED_COUNT = 20
DATA_FILE = Path(__file__).resolve().parent / "objects_mock.json"
ID_PATTERN = re.compile(r"^OBJ_\d{3}$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate camera scanner mock data JSON.")
    parser.add_argument("--input", type=Path, default=DATA_FILE, help="Input JSON file path.")
    parser.add_argument("--expected-count", type=int, default=EXPECTED_COUNT, help="Expected row count.")
    return parser.parse_args()


def validate_row(row: dict, index: int, seen_ids: set[str]) -> list[str]:
    errors: list[str] = []

    object_id = row.get("ObjectID")
    if not isinstance(object_id, str) or not ID_PATTERN.match(object_id):
        errors.append(f"Row {index}: ObjectID '{object_id}' invalid (expected OBJ_XXX)")
    elif object_id in seen_ids:
        errors.append(f"Row {index}: duplicate ObjectID '{object_id}'")
    else:
        seen_ids.add(object_id)

    object_type = row.get("ObjectType")
    if object_type not in {"Box_A", "Cylinder_B", "Irregular_C"}:
        errors.append(f"Row {index}: ObjectType '{object_type}' invalid")

    weight = row.get("Weight")
    if not isinstance(weight, (int, float)):
        errors.append(f"Row {index}: Weight must be numeric")
    elif not (0.1 <= float(weight) <= 10.0):
        errors.append(f"Row {index}: Weight {weight} out of range 0.1-10.0")

    if not isinstance(row.get("IsDefective"), bool):
        errors.append(f"Row {index}: IsDefective must be boolean")

    timestamp = row.get("ScanTimestamp")
    if not isinstance(timestamp, str):
        errors.append(f"Row {index}: ScanTimestamp must be string")
    else:
        try:
            datetime.fromisoformat(timestamp)
        except ValueError:
            errors.append(f"Row {index}: ScanTimestamp '{timestamp}' is not parseable ISO datetime")

    return errors


def main() -> None:
    args = parse_args()

    try:
        data = json.loads(args.input.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"ERROR: File not found -> {args.input}")
        sys.exit(1)
    except json.JSONDecodeError as exc:
        print(f"ERROR: Invalid JSON -> {exc}")
        sys.exit(1)

    if not isinstance(data, list):
        print("ERROR: Top-level JSON must be an array")
        sys.exit(1)

    errors: list[str] = []
    if len(data) != args.expected_count:
        errors.append(f"Expected {args.expected_count} rows but found {len(data)}")

    seen_ids: set[str] = set()
    for row_index, row in enumerate(data, start=1):
        if not isinstance(row, dict):
            errors.append(f"Row {row_index}: must be an object/dict")
            continue
        errors.extend(validate_row(row, row_index, seen_ids))

    if errors:
        print("FAIL:")
        for err in errors:
            print(f"- {err}")
        sys.exit(1)

    print(f"PASS: {args.expected_count}/{args.expected_count} rows valid")


if __name__ == "__main__":
    main()
