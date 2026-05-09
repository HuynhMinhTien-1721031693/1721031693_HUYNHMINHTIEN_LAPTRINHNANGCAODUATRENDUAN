# E2E Minimum Flow (Week 1)

This is the minimum wiring target for the first playable pass in `L_CameraScan_Test`.

## Blueprint event chain

1. `BP_MockDataManager` timer triggers `LoadNextObject`.
2. `LoadNextObject` spawns `BP_ScannableObjectBase` and sends to `BP_ConveyorBelt`.
3. Conveyor overlap with scan zone calls `BP_CameraScanner.BeginScan`.
4. Scanner finishes after `ScanDurationSeconds` and emits `OnScanCompleted`.
5. `BP_StateManager.RegisterScanResult` updates counters and sets `Classified`.
6. HUD handlers update state label and pass/fail counts.

## Required test logs

- `StateManager initialized`
- `Loaded row: OBJ_XXX`
- `Enter scan zone: OBJ_XXX`
- `Scan completed: OBJ_XXX pass/fail`
- `HUD updated: state + counters`

## Local non-UE verification

Run:

- `python "SmartFactory_CameraModule/Content/CameraModule/Tools/simulate_e2e_flow.py"`

Expected:

- Full 20-row cycle
- Final counters: `pass=16 fail=4 total=20`
