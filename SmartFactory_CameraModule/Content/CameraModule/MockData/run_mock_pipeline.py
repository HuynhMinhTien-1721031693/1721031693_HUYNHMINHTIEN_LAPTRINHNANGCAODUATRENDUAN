import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PY = sys.executable


def run_step(args: list[str]) -> None:
    print(f"[RUN] {' '.join(args)}")
    subprocess.run(args, check=True, cwd=ROOT)


def main() -> None:
    run_step([PY, "generate_mock_data.py", "--count", "20", "--defect-rate", "0.2", "--seed", "42"])
    run_step([PY, "validate_mock_data.py", "--expected-count", "20"])
    run_step([PY, "convert_for_ue_datatable.py"])
    print("Pipeline complete: objects_mock.json and objects_mock_ue_datatable.csv are ready.")


if __name__ == "__main__":
    main()
