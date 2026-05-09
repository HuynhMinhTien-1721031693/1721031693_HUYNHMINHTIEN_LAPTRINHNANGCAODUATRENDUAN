# Mock Data Schema (`objects_mock.json`)

Each row must contain:

- `ObjectID` (string, format `OBJ_XXX`)
- `ObjectType` (string, one of `Box_A`, `Cylinder_B`, `Irregular_C`)
- `Weight` (number, expected range `0.1 - 10.0`)
- `IsDefective` (boolean)
- `ScanTimestamp` (ISO-8601 string)

This schema maps directly to:

- CSV headers in `objects_mock_ue_datatable.csv`
- Unreal row struct `FScanObjectRow` (`ScanningDataTypes.h`)
