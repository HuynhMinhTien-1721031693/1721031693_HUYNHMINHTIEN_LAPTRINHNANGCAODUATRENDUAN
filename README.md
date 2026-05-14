# Smart Factory — Camera Scanning Module (UE5)

Dự án mô phỏng **nhà máy thông minh** với module **quét vật thể bằng camera** trong **Unreal Engine 5.7**, kết hợp **C++**, **Blueprint**, và **HTTP mock server** (Python) để mô phỏng luồng dữ liệu quét theo thời gian thực.

---

## Yêu cầu môi trường

| Thành phần | Ghi chú |
|-------------|---------|
| **Unreal Engine** | **5.7** (theo `EngineAssociation` trong `.uproject`) |
| **Visual Studio** | Build Tools / VS với workload **Game development with C++** (MSVC, Windows SDK) |
| **.NET** | Nếu build báo thiếu NetFxSDK, cài thêm **.NET Framework 4.8 SDK** qua Visual Studio Installer (Individual components) |
| **Python** | **3.x** (chạy mock server), lệnh `python` hoặc `py` |

---

## Cấu trúc thư mục (tổng quan)

```
PROJECT/
├── README.md                          ← tài liệu này
├── QA/                                ← checklist & mẫu báo cáo
│   ├── CAMERA_MODULE_WEEK1_ACCEPTANCE.md
│   ├── QA_CHECKLIST_PIE.md
│   └── REPORT_TEMPLATE.md
└── SmartFactory_CameraModule/         ← project UE chính
    ├── SmartFactory_CameraModule.uproject
    ├── SmartFactory_CameraModule.sln
    ├── camera_server.py               ← HTTP mock: /current, /status, /reset
    ├── Source/                        ← module C++ SmartFactory_CameraModule
    └── Content/CameraModule/          ← asset Blueprint, map, mock data, docs
```

Chi tiết layout nội dung trong UE: xem  
`SmartFactory_CameraModule/Content/CameraModule/README.md`.

---

## Mở project Unreal

1. Cài **UE 5.7** và đảm bảo association khớp với file `.uproject`.
2. Double-click  
   `SmartFactory_CameraModule/SmartFactory_CameraModule.uproject`  
   hoặc mở `SmartFactory_CameraModule.sln` rồi build **Development Editor** trước khi mở Editor.
3. Lần đầu hoặc sau khi sửa C++: Editor sẽ hỏi **rebuild modules** — chọn **Yes**.

---

## Mock HTTP server (Python)

Server cung cấp JSON giống pipeline thật, dùng file **`mock_scan_data.json`** (20 sự kiện quét).

### Chạy server

```powershell
cd SmartFactory_CameraModule
python camera_server.py
```

Hoặc: `py camera_server.py`

### Endpoint

| Path | Mô tả |
|------|--------|
| `GET http://localhost:8080/current` | JSON object hiện tại (canonical: `object_id`, `object_type`, `weight_kg`, `temperature_c`, `status`, `anomaly`, …) |
| `GET http://localhost:8080/status` | Tóm tắt thống kê mock |
| `GET http://localhost:8080/reset` | Reset index về đầu |

Server có luồng nền **tự advance** mock mỗi vài giây (`ADVANCE_SECONDS` trong `camera_server.py`) — log `[SCAN]` trong terminal là hành vi dự kiến.

### Vị trí file dữ liệu

`camera_server.py` tự tìm `mock_scan_data.json` theo thứ tự ưu tiên (trong code có `resolve_data_file()`). Thường dùng:

`SmartFactory_CameraModule/Content/CameraModule/MockData/mock_scan_data.json`

Công cụ Python bổ sung (validate, CSV cho DataTable, …) nằm trong  
`Content/CameraModule/MockData/`.

---

## Module C++ (`SmartFactory_CameraModule`)

- **`ScanningDataTypes.h`**: enum `EModuleState`, `EScanState`, struct payload quét (`FCurrentScanObject`), row DataTable (`FScanEventTableRow`), v.v.
- **`AStateManagerActor`**: Actor có thể dùng trong level; poll HTTP `GET {HttpBaseUrl}/current`, phân loại `status` + ngưỡng nhiệt độ, optional fallback **DataTable**, phím **1–6** để debug state.

### Blueprint kế thừa C++ (khuyến nghị khi cần dữ liệu thật từ server)

1. **Content Browser** → **Blueprint Class** → **All Classes** → tìm **`StateManagerActor`**.
2. Tạo ví dụ `BP_StateManager_HTTP`.
3. **Class Defaults**: `Http Base Url` = `http://127.0.0.1:8080`, bật HTTP polling, chỉnh `Poll Interval Seconds` nếu cần.
4. Kéo actor vào level, **Play** khi `camera_server.py` đang chạy.

> **Lưu ý:** Blueprint **Actor** thuần (`Parent = Actor`) **không có sẵn** node HTTP GET trong graph; muốn HTTP hoàn toàn trong Blueprint cần plugin bên thứ ba hoặc hàm C++ `BlueprintCallable` tùy chỉnh.

---

## Blueprint học tập (`BP_StateManager`)

Có thể dùng Blueprint **Actor** `BP_StateManager` để luyện:

- Biến trạng thái (`EModuleState`, counters),
- `Event BeginPlay` + **Set Timer by Function Name** (`ScanCycle`, `CompleteScan`, `ResetToIdle`),
- Phím **1–6** + `Auto Receive Input = Player 0` trên actor trong level.

Luồng thiết kế đầy đủ hơn (MockDataManager → Conveyor → Scanner → HUD) được mô tả trong  
`Content/CameraModule/Docs/DATA_FLOW.md` và các file trong `Content/CameraModule/Docs/`.

---

## QA & báo cáo

- `QA/CAMERA_MODULE_WEEK1_ACCEPTANCE.md` — tiêu chí nghiệm thu.
- `QA/QA_CHECKLIST_PIE.md` — checklist PIE.
- `QA/REPORT_TEMPLATE.md` — mẫu báo cáo.

---

## Build từ dòng lệnh (tùy chọn)

Nếu đã cài UE tại `D:\UE_5.7` (điều chỉnh đường dẫn cho máy bạn):

```powershell
"D:\UE_5.7\Engine\Build\BatchFiles\Build.bat" SmartFactory_CameraModuleEditor Win64 Development ".\SmartFactory_CameraModule\SmartFactory_CameraModule.uproject" -WaitMutex
```

---

## Git

```powershell
git clone <URL-repo>
cd PROJECT
```

Sau chỉnh sửa: `git add`, `git commit`, `git push` theo quy ước nhóm.

---

## Tác giả / môn học

Dự án phục vụ môn **Lập trình nâng cao dựa trên dự án** — module camera scanning trong bối cảnh Smart Factory.

---

## License

Nội dung theo quy định repository / giảng viên môn học (bổ sung nếu có file `LICENSE` riêng).
