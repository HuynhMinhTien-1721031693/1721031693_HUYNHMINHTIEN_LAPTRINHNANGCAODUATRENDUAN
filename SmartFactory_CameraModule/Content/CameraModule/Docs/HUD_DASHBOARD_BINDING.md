# HUD/Dashboard Binding Guide

This guide defines minimal `WBP_ScannerHUD` bindings for week-1 delivery.

## Widget fields

- `txtCurrentState`
- `txtCurrentObjectID`
- `txtPassCount`
- `txtFailCount`
- `txtThroughput`

## Binding sequence

1. On `Event Construct`, get `BP_StateManager` and `BP_CameraScanner` references.
2. Bind `BP_StateManager.OnStateChanged` -> `HandleStateChanged`.
3. Bind `BP_StateManager.OnCountersUpdated` -> `HandleCountersUpdated`.
4. Bind `BP_CameraScanner.OnScanCompleted` -> `HandleScanCompleted`.

## Suggested handlers

- `HandleStateChanged(PreviousState, NewState)`
  - Update `txtCurrentState`
- `HandleCountersUpdated(PassCount, FailCount)`
  - Update `txtPassCount` and `txtFailCount`
- `HandleScanCompleted(ObjectID, IsDefective)`
  - Update `txtCurrentObjectID`
  - Optional: flash status color for pass/fail

## Throughput formula

- `ThroughputPerMinute = ProcessedCount / ElapsedMinutes`
- Display `ProcessedCount` if elapsed time < 60 seconds.
