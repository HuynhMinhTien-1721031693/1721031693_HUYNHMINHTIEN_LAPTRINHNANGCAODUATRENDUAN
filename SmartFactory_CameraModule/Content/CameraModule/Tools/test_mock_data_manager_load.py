import csv
from pathlib import Path


CSV_FILE = Path(__file__).resolve().parents[1] / "MockData" / "objects_mock_ue_datatable.csv"
PREVIEW_COUNT = 5


def main() -> None:
    with CSV_FILE.open("r", encoding="utf-8") as csv_file:
        rows = list(csv.DictReader(csv_file))

    if len(rows) < PREVIEW_COUNT:
        raise RuntimeError(f"Expected at least {PREVIEW_COUNT} rows, found {len(rows)}.")

    print(f"Loaded {len(rows)} rows from {CSV_FILE.name}")
    print(f"Previewing first {PREVIEW_COUNT} rows (MockDataManager LoadNextObject contract):")
    for index, row in enumerate(rows[:PREVIEW_COUNT], start=1):
        object_id = row.get("ObjectID", "")
        object_type = row.get("ObjectType", "")
        is_defective = row.get("IsDefective", "")
        scan_timestamp = row.get("ScanTimestamp", "")
        print(
            f"{index:02d}. ObjectID={object_id} "
            f"ObjectType={object_type} IsDefective={is_defective} "
            f"ScanTimestamp={scan_timestamp}"
        )


if __name__ == "__main__":
    main()
