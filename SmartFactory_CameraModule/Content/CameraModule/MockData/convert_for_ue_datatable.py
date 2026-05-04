import json
from pathlib import Path


INPUT_FILE = Path(__file__).resolve().parent / "mock_scan_data.json"
OUTPUT_FILE = Path(__file__).resolve().parent / "mock_scan_data_ue_datatable.json"


def main() -> None:
    source = json.loads(INPUT_FILE.read_text(encoding="utf-8"))
    rows = []
    for idx, item in enumerate(source, start=1):
        size = item.get("size_cm", {})
        row_name = item.get("object_id") or f"Row_{idx:03d}"
        rows.append(
            {
                "Name": row_name,
                "ObjectID": item.get("object_id", ""),
                "ObjectType": item.get("object_type", ""),
                "SizeW": float(size.get("w", 0.0)),
                "SizeH": float(size.get("h", 0.0)),
                "SizeD": float(size.get("d", 0.0)),
                "WeightKg": float(item.get("weight_kg", 0.0)),
                "TemperatureC": float(item.get("temperature_c", 0.0)),
                "Timestamp": item.get("timestamp", ""),
                "Status": item.get("status", ""),
                "HasAnomaly": item.get("anomaly") is not None,
            }
        )

    OUTPUT_FILE.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    print(f"Converted {len(rows)} rows")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
