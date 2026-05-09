import csv
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


CSV_FILE = Path(__file__).resolve().parents[1] / "MockData" / "objects_mock_ue_datatable.csv"
SIMULATION_ROWS = 20


class ScanState(str, Enum):
    IDLE = "Idle"
    CONVEYOR_RUNNING = "ConveyorRunning"
    OBJECT_DETECTED = "ObjectDetected"
    SCANNING = "Scanning"
    CLASSIFIED = "Classified"
    ERROR = "Error"


@dataclass
class ScanObject:
    object_id: str
    object_type: str
    is_defective: bool
    scan_timestamp: str


def load_rows(limit: int) -> list[ScanObject]:
    with CSV_FILE.open("r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        rows: list[ScanObject] = []
        for row in reader:
            rows.append(
                ScanObject(
                    object_id=row["ObjectID"],
                    object_type=row["ObjectType"],
                    is_defective=row["IsDefective"].strip().lower() == "true",
                    scan_timestamp=row["ScanTimestamp"],
                )
            )
            if len(rows) >= limit:
                break
    return rows


def main() -> None:
    rows = load_rows(SIMULATION_ROWS)
    if not rows:
        raise RuntimeError("No rows loaded. Run mock pipeline first.")

    pass_count = 0
    fail_count = 0
    state = ScanState.IDLE
    print(f"[STATE] {state.value}")

    for row in rows:
        state = ScanState.CONVEYOR_RUNNING
        print(f"[STATE] {state.value} | Object {row.object_id} on belt")

        state = ScanState.OBJECT_DETECTED
        print(f"[STATE] {state.value} | Object {row.object_id} in scan zone")

        state = ScanState.SCANNING
        print(f"[STATE] {state.value} | Scanning {row.object_id} ({row.object_type})")

        state = ScanState.CLASSIFIED
        if row.is_defective:
            fail_count += 1
            result = "FAIL"
        else:
            pass_count += 1
            result = "PASS"
        print(f"[STATE] {state.value} | Result={result} ObjectID={row.object_id}")

    print(f"[HUD] Final counters: pass={pass_count} fail={fail_count} total={len(rows)}")


if __name__ == "__main__":
    main()
