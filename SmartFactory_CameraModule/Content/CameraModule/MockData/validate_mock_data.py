import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


DATA_FILE = Path(__file__).resolve().parent / "mock_scan_data.json"
REQUIRED_FIELDS = {
    "object_id",
    "object_type",
    "size_cm",
    "weight_kg",
    "temperature_c",
    "timestamp",
    "status",
    "anomaly",
}
VALID_STATUSES = {"ok", "warning", "error"}
VALID_TYPES = {"box_A", "box_B", "pallet", "unknown"}


def pass_fail(condition: bool, pass_msg: str, fail_msg: str) -> bool:
    if condition:
        print(f"[PASS] {pass_msg}")
        return True
    print(f"[FAIL] {fail_msg}")
    return False


def parse_timestamp(ts: str) -> datetime:
    # Input example: 2025-06-01T08:00:00Z
    return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")


def preview_table(items: List[Dict[str, Any]]) -> None:
    print("\nPreview:")
    print("# | object_id      | type    | weight  | temp   | status   | anomaly")
    print("--|----------------|---------|---------|--------|----------|---------------")
    for idx, obj in enumerate(items, start=1):
        anomaly = obj["anomaly"] if obj["anomaly"] is not None else "null"
        row = (
            f"{idx:>2} | "
            f"{str(obj['object_id']):<14} | "
            f"{str(obj['object_type']):<7} | "
            f"{float(obj['weight_kg']):>6.2f} kg | "
            f"{float(obj['temperature_c']):>5.1f}C | "
            f"{str(obj['status']):<8} | "
            f"{anomaly}"
        )
        print(row)


def main() -> None:
    all_ok = True

    # 1) File loads as valid JSON
    try:
        raw = DATA_FILE.read_text(encoding="utf-8")
        data = json.loads(raw)
        all_ok &= pass_fail(True, "File loads as valid JSON", "File is not valid JSON")
    except Exception as exc:
        pass_fail(False, "", f"Could not load JSON file: {exc}")
        return

    # 2) Exactly 20 objects in array
    is_list = isinstance(data, list)
    all_ok &= pass_fail(is_list, "Top-level JSON is an array", "Top-level JSON is not an array")
    if not is_list:
        return

    all_ok &= pass_fail(
        len(data) == 20,
        "All 20 objects present",
        f"Expected 20 objects but found {len(data)}",
    )

    # 3) Required fields present in every object
    missing_field_issues = []
    for i, obj in enumerate(data, start=1):
        if not isinstance(obj, dict):
            missing_field_issues.append(f"Item #{i} is not an object")
            continue
        missing = REQUIRED_FIELDS - obj.keys()
        if missing:
            missing_field_issues.append(f"Item #{i} missing: {sorted(missing)}")

    all_ok &= pass_fail(
        len(missing_field_issues) == 0,
        "All fields present",
        "One or more objects missing required fields",
    )
    if missing_field_issues:
        for issue in missing_field_issues[:5]:
            print(f"  - {issue}")

    # 4) status values valid
    bad_status = [
        (i + 1, obj.get("status"))
        for i, obj in enumerate(data)
        if isinstance(obj, dict) and obj.get("status") not in VALID_STATUSES
    ]
    all_ok &= pass_fail(
        len(bad_status) == 0,
        'All statuses are in {"ok","warning","error"}',
        f"Found invalid status values: {bad_status[:5]}",
    )

    # 5) object_type values valid
    bad_types = [
        (i + 1, obj.get("object_type"))
        for i, obj in enumerate(data)
        if isinstance(obj, dict) and obj.get("object_type") not in VALID_TYPES
    ]
    all_ok &= pass_fail(
        len(bad_types) == 0,
        'All object types are in {"box_A","box_B","pallet","unknown"}',
        f"Found invalid object_type values: {bad_types[:5]}",
    )

    # 6) At least 1 warning
    warning_count = sum(1 for obj in data if isinstance(obj, dict) and obj.get("status") == "warning")
    all_ok &= pass_fail(
        warning_count >= 1,
        f"Found warning objects ({warning_count})",
        "No warning object found",
    )

    # 7) At least 1 error
    error_count = sum(1 for obj in data if isinstance(obj, dict) and obj.get("status") == "error")
    all_ok &= pass_fail(
        error_count >= 1,
        f"Found error objects ({error_count})",
        "No error object found",
    )

    # 8) At least 1 fire_thermal anomaly
    fire_count = sum(1 for obj in data if isinstance(obj, dict) and obj.get("anomaly") == "fire_thermal")
    all_ok &= pass_fail(
        fire_count >= 1,
        f"Found fire_thermal anomalies ({fire_count})",
        "No fire_thermal anomaly found",
    )

    # 9) Timestamps ascending
    timestamp_ok = True
    parsed_times = []
    for i, obj in enumerate(data, start=1):
        try:
            parsed_times.append(parse_timestamp(str(obj.get("timestamp"))))
        except Exception:
            timestamp_ok = False
            print(f"  - Invalid timestamp format at item #{i}: {obj.get('timestamp')}")
            break
    if timestamp_ok and any(parsed_times[i] > parsed_times[i + 1] for i in range(len(parsed_times) - 1)):
        timestamp_ok = False
    all_ok &= pass_fail(
        timestamp_ok,
        "Timestamps are in ascending order",
        "Timestamps are not in ascending order",
    )

    # 10) weight_kg in range 1..100
    bad_weights = []
    for i, obj in enumerate(data, start=1):
        try:
            w = float(obj.get("weight_kg"))
            if not (1.0 <= w <= 100.0):
                bad_weights.append((i, w))
        except Exception:
            bad_weights.append((i, obj.get("weight_kg")))

    all_ok &= pass_fail(
        len(bad_weights) == 0,
        "All weight_kg values are in realistic range (1-100)",
        f"Found out-of-range or invalid weights: {bad_weights[:5]}",
    )

    preview_table(data)

    print("\nValidation Result:")
    if all_ok:
        print("[PASS] Dataset is valid for Camera Scanning module")
    else:
        print("[FAIL] Dataset has validation issues (see checks above)")


if __name__ == "__main__":
    main()
