# Camera Module Week 1 Acceptance

## Pre-run

1. Regenerate data:
   - `python "SmartFactory_CameraModule/Content/CameraModule/MockData/run_mock_pipeline.py"`
2. Sanity-check first 5 rows:
   - `python "SmartFactory_CameraModule/Content/CameraModule/Tools/test_mock_data_manager_load.py"`
3. Optional local simulation:
   - `python "SmartFactory_CameraModule/Content/CameraModule/Tools/simulate_e2e_flow.py"`

## PIE acceptance checklist (`L_CameraScan_Test`)

| ID | Check | Pass Criteria | Evidence |
| --- | --- | --- | --- |
| CAM-001 | DataTable import | `DT_MockScanObjects` has 20 rows | Screenshot/DataTable preview |
| CAM-002 | Mock spawn | `BP_MockDataManager` spawns objects in order `OBJ_001..` | Output Log |
| CAM-003 | Conveyor trigger | `OnObjectEnterScanZone` fires for each object | Output Log |
| CAM-004 | Scan result | `BP_CameraScanner` emits completed event with correct `IsDefective` | Output Log |
| CAM-005 | State transitions | `Idle -> ConveyorRunning -> ObjectDetected -> Scanning -> Classified` | Output Log |
| CAM-006 | HUD state binding | `WBP_ScannerHUD` reflects current state in real-time | PIE capture |
| CAM-007 | HUD counters | Pass/Fail counters match processed objects | PIE capture |
| CAM-008 | Stability | Full 20-object run without crash | Output Log |

## Mapping to existing QA IDs

- `CAM-001` aligns with `QA-007`
- `CAM-002` aligns with `QA-008`
- `CAM-005` aligns with `QA-004` and `QA-005`
- `CAM-006` aligns with `QA-009`
- `CAM-008` aligns with `QA-010`
