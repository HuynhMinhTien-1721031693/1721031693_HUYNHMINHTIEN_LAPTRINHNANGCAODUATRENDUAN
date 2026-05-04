import json
import random
from pathlib import Path


OUTPUT_COUNT = 20
OBJECT_TYPES = ("Box", "Cylinder", "Pallet")
OUTPUT_FILE = Path(__file__).resolve().parent / "mock_scan_data.json"


def generate_row(index: int) -> dict:
    object_id = f"OBJ-{index + 1:03d}"
    return {
        "Name": object_id,  # Unreal DataTable row name
        "ObjectID": object_id,
        "ObjectType": random.choice(OBJECT_TYPES),
        "ScanDuration": round(random.uniform(1.5, 5.0), 1),
        "Weight": round(random.uniform(10.0, 100.0), 2),
        "IsValid": random.random() < 0.8,
    }


def validate_row_count(items: list[dict], expected_count: int = OUTPUT_COUNT) -> bool:
    return len(items) == expected_count


def main() -> None:
    rows = [generate_row(i) for i in range(OUTPUT_COUNT)]
    OUTPUT_FILE.write_text(json.dumps(rows, indent=2), encoding="utf-8")

    is_valid = validate_row_count(rows)
    print(f"Generated {len(rows)} rows")
    print(f"Output file: {OUTPUT_FILE}")
    print(f"Validation: {'PASS' if is_valid else 'FAIL'} (expected {OUTPUT_COUNT})")


if __name__ == "__main__":
    main()
