import json
import random
import sys
import argparse
from datetime import datetime, timedelta
from pathlib import Path


OUTPUT_COUNT = 20
OBJECT_TYPES = ("Box_A", "Cylinder_B", "Irregular_C")
DEFECT_RATE = 0.2
OUTPUT_FILE = Path(__file__).resolve().parent / "objects_mock.json"
BASE_TIMESTAMP = datetime(2025, 1, 1, 0, 0, 0)


def generate_row(index: int, defective_indices: set[int]) -> dict:
    timestamp = BASE_TIMESTAMP + timedelta(minutes=index)
    return {
        "ObjectID": f"OBJ_{index + 1:03d}",
        "ObjectType": random.choice(OBJECT_TYPES),
        "Weight": round(random.uniform(0.5, 5.0), 2),
        "IsDefective": index in defective_indices,
        "ScanTimestamp": timestamp.isoformat(),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate camera scanning mock data JSON.")
    parser.add_argument("--count", type=int, default=OUTPUT_COUNT, help="Number of rows to generate.")
    parser.add_argument(
        "--defect-rate",
        type=float,
        default=DEFECT_RATE,
        help="Defective ratio from 0.0 to 1.0.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for deterministic output.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=OUTPUT_FILE,
        help="Output JSON file path.",
    )
    return parser.parse_args()


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    args = parse_args()

    if args.count <= 0:
        raise ValueError("--count must be > 0")
    if not (0.0 <= args.defect_rate <= 1.0):
        raise ValueError("--defect-rate must be between 0.0 and 1.0")

    random.seed(args.seed)
    defective_count = int(args.count * args.defect_rate)
    defective_indices = set(random.sample(range(args.count), k=defective_count))
    rows = [generate_row(i, defective_indices) for i in range(args.count)]
    args.output.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    print(f"Generated {args.count} objects -> {args.output.name} (seed={args.seed})")


if __name__ == "__main__":
    main()
