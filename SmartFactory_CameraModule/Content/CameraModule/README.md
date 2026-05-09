# CameraModule Content Layout

This folder contains all assets for the Camera Object Scanning module.

## Recommended layout

- `Core/`: shared data types, state assets, and scanner configs
- `Actors/`: gameplay actors (`BP_CameraScanner`, `BP_StateManager`, `BP_MockDataManager`, `BP_ConveyorBelt`)
- `UI/`: widgets (`WBP_ScannerHUD`, row/state child widgets)
- `Data/`: DataTable assets and import-ready CSV files
- `MockData/`: source JSON/CSV and python tools for regeneration
- `Materials/`, `Meshes/`, `Textures/`: visuals dedicated to this module
- `Maps/`: test map (`L_CameraScan_Test`) and module-only scenes
- `Tools/`: editor/python helpers used to bootstrap assets
- `Docs/`: implementation contracts for Blueprint graph wiring

## Naming convention

- Blueprint classes: `BP_*`
- Widgets: `WBP_*`
- Data tables: `DT_*`
- Structs: `ST_*`
- Enums: `E_*`
- Data assets: `DA_*`
