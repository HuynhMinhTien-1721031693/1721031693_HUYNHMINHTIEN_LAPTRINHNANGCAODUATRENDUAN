import json
import random
from datetime import datetime, timedelta, timezone


OBJECT_TYPES = ["box_A", "box_B", "pallet", "unknown"]

SIZE_RANGES_CM = {
    "box_A": {"w": (20, 40), "h": (15, 35), "d": (20, 40)},
    "box_B": {"w": (35, 65), "h": (25, 50), "d": (35, 65)},
    "pallet": {"w": (80, 120), "h": (12, 25), "d": (100, 140)},
    "unknown": {"w": (15, 140), "h": (10, 90), "d": (15, 160)},
}

WEIGHT_RANGES_KG = {
    "box_A": (3.0, 8.0),
    "box_B": (8.0, 15.0),
    "pallet": (20.0, 50.0),
    "unknown": (1.0, 60.0),
}

TYPE_MAX_WEIGHT_KG = {
    "box_A": 8.0,
    "box_B": 15.0,
    "pallet": 50.0,
}

STATUS_WEIGHTS = [("ok", 0.7), ("warning", 0.2), ("error", 0.1)]

START_TS = datetime(2025, 1, 1, 8, 0, 0, tzinfo=timezone.utc)
EVENT_COUNT = 20
STEP_SECONDS = 30
OUTPUT_FILE = "mock_scan_data.json"


def weighted_status() -> str:
    statuses = [item[0] for item in STATUS_WEIGHTS]
    weights = [item[1] for item in STATUS_WEIGHTS]
    return random.choices(statuses, weights=weights, k=1)[0]


def random_size_cm(object_type: str) -> dict:
    ranges = SIZE_RANGES_CM[object_type]
    return {
        "w": random.randint(*ranges["w"]),
        "h": random.randint(*ranges["h"]),
        "d": random.randint(*ranges["d"]),
    }


def random_weight_kg(object_type: str) -> float:
    min_w, max_w = WEIGHT_RANGES_KG[object_type]
    return round(random.uniform(min_w, max_w), 2)


def random_temperature_c() -> float:
    # Mostly normal range, occasional anomaly spikes for testing.
    is_hot = random.random() < 0.15
    if is_hot:
        return round(random.uniform(60.0, 90.0), 2)
    return round(random.uniform(20.0, 28.0), 2)


def build_event(index: int) -> dict:
    object_type = random.choice(OBJECT_TYPES)
    event_time = START_TS + timedelta(seconds=index * STEP_SECONDS)

    event = {
        "object_id": f"OBJ-{index + 1:03d}",
        "object_type": object_type,
        "size_cm": random_size_cm(object_type),
        "weight_kg": random_weight_kg(object_type),
        "temperature_c": random_temperature_c(),
        "timestamp": event_time.isoformat().replace("+00:00", "Z"),
        "status": weighted_status(),
        "anomaly": None,
    }

    # Validation rule 1: overweight relative to type max => warning.
    type_max = TYPE_MAX_WEIGHT_KG.get(object_type)
    if type_max is not None and event["weight_kg"] > type_max:
        event["status"] = "warning"

    # Validation rule 2: unknown objects => warning.
    if object_type == "unknown":
        event["status"] = "warning"

    # Validation rule 3: high temperature => fire anomaly + error.
    if event["temperature_c"] > 55.0:
        event["anomaly"] = "fire_thermal"
        event["status"] = "error"

    # Validation rule 4: random hardware fault => error + fault ID.
    if random.random() < 0.05:
        event["status"] = "error"
        event["object_id"] = "ERR-FAULT"

    return event


def summarize(events: list[dict]) -> dict:
    counts = {"ok": 0, "warning": 0, "error": 0, "anomaly": 0}
    for event in events:
        status = event["status"]
        counts[status] += 1
        if event["anomaly"] is not None:
            counts["anomaly"] += 1
    return counts


def main() -> None:
    events = [build_event(i) for i in range(EVENT_COUNT)]

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(events, f, ensure_ascii=False, indent=2)

    summary = summarize(events)
    print(f"Saved {len(events)} events to {OUTPUT_FILE}")
    print(
        "Summary: "
        f"ok={summary['ok']}, "
        f"warning={summary['warning']}, "
        f"error={summary['error']}, "
        f"anomaly={summary['anomaly']}"
    )


if __name__ == "__main__":
    main()
