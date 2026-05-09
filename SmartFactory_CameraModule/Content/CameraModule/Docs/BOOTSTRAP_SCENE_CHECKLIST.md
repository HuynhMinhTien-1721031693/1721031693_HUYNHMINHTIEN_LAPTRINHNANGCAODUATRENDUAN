# Bootstrap Scene Checklist (`L_CameraScan_Test`)

Use this as the exact order for first Blueprint assembly in Editor.

## 1. Create core assets

1. Create enum `E_ScanState` with values:
   - `Idle`
   - `ConveyorRunning`
   - `ObjectDetected`
   - `Scanning`
   - `Classified`
   - `Error`
2. Create struct `ST_ScanObject`:
   - `ObjectID` (`Name`)
   - `ObjectType` (`Name`)
   - `Weight` (`Float`)
   - `IsDefective` (`Bool`)
   - `ScanTimestamp` (`String`)
3. Create data asset `DA_ScannerConfig`:
   - `ScanDurationSeconds`
   - `ConveyorSpeedCmPerSec`
   - `SpawnIntervalSeconds`
   - `bAutoCycle`

## 2. Import DataTable

1. Create `DT_MockScanObjects` in `Data/`.
2. Row struct: `ST_ScanObject`.
3. Import CSV: `MockData/objects_mock_ue_datatable.csv`.
4. Verify row count is 20.

## 3. Create actor Blueprints

1. `BP_StateManager` (base: Actor)
2. `BP_MockDataManager` (base: Actor)
3. `BP_ConveyorBelt` (base: Actor)
4. `BP_CameraScanner` (base: Actor)
5. `BP_ScannableObjectBase` (base: Actor)

Use contracts in `BLUEPRINT_CONTRACTS.md` for variable names, dispatchers, and function signatures.

## 4. Create test map and wire references

1. Create map `L_CameraScan_Test`.
2. Place all four manager actors into map.
3. Assign references:
   - `BP_MockDataManager.MockDataTable = DT_MockScanObjects`
   - `BP_CameraScanner.ScannerConfig = DA_ScannerConfig`
4. Add temporary log prints to every dispatcher call.

## 5. Add HUD

1. Create `WBP_ScannerHUD`.
2. Add text blocks:
   - `CurrentState`
   - `CurrentObjectID`
   - `PassCount`
   - `FailCount`
3. Bind on `BeginPlay` to state/scanner dispatchers.
