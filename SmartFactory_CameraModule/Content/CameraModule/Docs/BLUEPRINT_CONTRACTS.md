# Blueprint Contracts (Week 1 Bootstrap)

This file is the implementation contract for the first UE5 Blueprint pass.

## `BP_CameraScanner` (Actor)

### Required components
- `SceneRoot`
- `ScanZone` (`BoxCollision`)
- `ScanMarker` (`Billboard` or mesh for debug)

### Exposed variables
- `ScannerConfig` (`DA_ScannerConfig`)
- `CurrentObjectID` (`Name`)
- `CurrentObjectType` (`Name`)
- `CurrentIsDefective` (`bool`)
- `ScanDurationSeconds` (`float`)

### Event dispatchers
- `OnScanStarted(ObjectID)`
- `OnScanCompleted(ObjectID, IsDefective)`
- `OnScanError(ObjectID, ErrorMessage)`

### Public functions
- `BeginScan(ObjectMeta)`
- `CompleteScan()`
- `AbortScan(ErrorMessage)`

## `BP_StateManager` (Actor)

### Exposed variables
- `CurrentState` (`E_ScanState`)
- `LastStateChangeTime` (`DateTime`)
- `PassCount` (`int`)
- `FailCount` (`int`)

### Event dispatchers
- `OnStateChanged(PreviousState, NewState)`
- `OnCountersUpdated(PassCount, FailCount)`

### Public functions
- `SetState(NewState)`
- `RegisterScanResult(IsDefective)`

## `BP_MockDataManager` (Actor)

### Exposed variables
- `MockDataTable` (`DT_MockScanObjects`)
- `SpawnClass` (`BP_ScannableObjectBase`)
- `CurrentRowIndex` (`int`)
- `AutoSpawnInterval` (`float`)

### Event dispatchers
- `OnObjectSpawned(ObjectID, SpawnedActor)`
- `OnDataExhausted()`

### Public functions
- `InitializeFromDataTable()`
- `LoadNextObject()`
- `ResetStream()`

## `BP_ConveyorBelt` (Actor)

### Exposed variables
- `BeltSpeedCmPerSec` (`float`)
- `ScanZoneTrigger` (`BoxCollision`)

### Event dispatchers
- `OnObjectEnterScanZone(ObjectActor)`
- `OnObjectExitScanZone(ObjectActor)`

### Public functions
- `StartConveyor()`
- `StopConveyor()`
- `SetConveyorSpeed(NewSpeed)`

## `WBP_ScannerHUD` (Widget)

### Bound values
- `CurrentStateText`
- `CurrentObjectIDText`
- `PassFailCounterText`
- `ThroughputText`

### Required widget events
- `BindToStateManager(StateManagerRef)`
- `BindToScanner(ScannerRef)`
- `RefreshHUD()`

## Runtime sequence (minimum viable)

1. `BP_MockDataManager` calls `LoadNextObject()`.
2. Spawned object enters `BP_ConveyorBelt`.
3. Conveyor overlap triggers `OnObjectEnterScanZone`.
4. `BP_CameraScanner` calls `BeginScan`, then `CompleteScan`.
5. `BP_StateManager` receives scan result and updates counters/state.
6. `WBP_ScannerHUD` reacts to dispatchers and updates labels.
