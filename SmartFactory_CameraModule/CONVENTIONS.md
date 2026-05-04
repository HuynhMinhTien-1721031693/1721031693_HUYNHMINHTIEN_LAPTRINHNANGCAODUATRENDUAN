# Smart Factory UE5 Conventions

## Naming Rules
- Blueprint assets: `BP_` prefix (example: `BP_StateManager`)
- DataTable assets: `DT_` prefix (example: `DT_MockScanData`)
- Enum types/assets: `E_` prefix (example: `E_ModuleState`)
- Struct types/assets: `F_` prefix (example: `F_ObjectData`)

## Folder Ownership
- TV1 = Core
- TV2 = Environment
- TV3 = Gameplay
- TV4 = Data
- TV5 = UI
- TV6 = QA

## Git Commit Message Format
- Required format: `[TV1] feat: mo ta ngan`
- Examples:
  - `[TV3] feat: add state manager transitions`
  - `[TV4] feat: add mock scan datatable import script`
