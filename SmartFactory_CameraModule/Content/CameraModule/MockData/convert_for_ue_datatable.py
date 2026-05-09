import csv
import json
import argparse
from pathlib import Path


INPUT_FILE = Path(__file__).resolve().parent / "objects_mock.json"
OUTPUT_FILE = Path(__file__).resolve().parent / "objects_mock_ue_datatable.csv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert mock JSON into UE DataTable CSV.")
    parser.add_argument("--input", type=Path, default=INPUT_FILE, help="Input JSON file path.")
    parser.add_argument("--output", type=Path, default=OUTPUT_FILE, help="Output CSV file path.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source = json.loads(args.input.read_text(encoding="utf-8"))
    fieldnames = ["Name", "ObjectID", "ObjectType", "Weight", "IsDefective", "ScanTimestamp"]

    with args.output.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for idx, item in enumerate(source, start=1):
            row_name = f"Row_{idx:03d}"
            writer.writerow(
                {
                    "Name": row_name,
                    "ObjectID": item.get("ObjectID", ""),
                    "ObjectType": item.get("ObjectType", ""),
                    "Weight": item.get("Weight", 0.0),
                    "IsDefective": str(bool(item.get("IsDefective", False))),
                    "ScanTimestamp": item.get("ScanTimestamp", ""),
                }
            )

    print(f"Converted {len(source)} rows -> {args.output.name}")


if __name__ == "__main__":
    main()
