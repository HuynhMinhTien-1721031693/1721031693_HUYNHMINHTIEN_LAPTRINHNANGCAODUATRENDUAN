# QA Checklist PIE - UE5 Hệ thống phân loại hàng hóa

## Hướng dẫn sử dụng

> Mục tiêu: Ghi nhận kết quả test PIE theo từng build một cách nhất quán, để đối chiếu nhanh với báo cáo tuần trong `REPORT_TEMPLATE.md`.

- Điền đầy đủ tất cả cột trước khi chốt kết quả buổi test.
- Cột `Status` chỉ được chọn một giá trị: `Pass`, `Fail`, hoặc `N/A`.
- Cột `Evidence` phải kèm đường dẫn log, screenshot, video, hoặc ticket bug (nếu `Fail`).
- Cột `Build/Commit` sử dụng format khuyến nghị: `vX.Y.Z+<short_sha>`.
- Cột `Run Date` sử dụng định dạng: `yyyy-mm-dd`.
- Mỗi test case có `ID` trùng với Demo Checklist trong `REPORT_TEMPLATE.md`.

## Bảng checklist

| ID | Test Case | Steps (1-3 bước) | Expected Result | Actual Result | Status (Pass/Fail/N/A) | Evidence | Environment | Build/Commit | Run Date | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| QA-001 | Scene load không crash | 1) Mở UE5 project. 2) Chạy Play-In-Editor (PIE) tại map chính. 3) Theo dõi log trong 30 giây đầu. | Scene load thành công, không crash editor/game instance, không có critical error. | [Điền kết quả thực tế] | [Pass/Fail/N/A] | [Link log/screenshot/video] | [VD: Win11 + RTX3060 + PIE] | [vX.Y.Z+sha] | [yyyy-mm-dd] | TV1 |
| QA-002 | FPS idle > 60 | 1) Bật PIE tại scene chính. 2) Không thao tác trong 60 giây. 3) Dùng `stat fps` để ghi nhận. | FPS trung bình > 60 khi idle, không có sụt giảm bất thường. | [Điền kết quả thực tế] | [Pass/Fail/N/A] | [Link metric/log] | [VD: Win11 + RTX3060 + Epic] | [vX.Y.Z+sha] | [yyyy-mm-dd] | TV2 |
| QA-003 | StateManager initialized log | 1) Bật PIE. 2) Mở Output Log. 3) Tìm chuỗi `initialized` của StateManager. | StateManager khởi tạo thành công và in log chứa `initialized`. | [Điền kết quả thực tế] | [Pass/Fail/N/A] | [Link log] | [Môi trường test] | [vX.Y.Z+sha] | [yyyy-mm-dd] | TV3 |
| QA-004 | Trigger Idle -> Scanning | 1) Bật PIE ở state Idle. 2) Kích hoạt hành động bắt đầu scan. 3) Theo dõi state transition trên log/UI. | Hệ thống transition từ Idle sang Scanning đúng trigger đã định nghĩa. | [Điền kết quả thực tế] | [Pass/Fail/N/A] | [Link log/video] | [Môi trường test] | [vX.Y.Z+sha] | [yyyy-mm-dd] | TV4 |
| QA-005 | Trigger Scanning -> Detected | 1) Trong state Scanning, đưa vật thể hợp lệ vào luồng xử lý. 2) Chờ hệ thống nhận diện. 3) Kiểm tra state mới. | State chuyển từ Scanning sang Detected đúng điều kiện trigger. | [Điền kết quả thực tế] | [Pass/Fail/N/A] | [Link log/video] | [Môi trường test] | [vX.Y.Z+sha] | [yyyy-mm-dd] | TV5 |
| QA-006 | Trigger transition sang Error | 1) Bật PIE. 2) Cấp input lỗi (dữ liệu hỏng/sai format). 3) Theo dõi state và log lỗi. | Hệ thống transition sang Error đúng trigger input lỗi, có log lỗi rõ ràng. | [Điền kết quả thực tế] | [Pass/Fail/N/A] | [Link log/ticket bug] | [Môi trường test] | [vX.Y.Z+sha] | [yyyy-mm-dd] | TV6 |
| QA-007 | DataTable load 20 rows | 1) Bật PIE và gọi luồng load DataTable. 2) Kiểm tra số row sau khi load. 3) Theo dõi warning/error. | DataTable load đủ 20 rows, không warning/error liên quan đến DataTable. | [Điền kết quả thực tế] | [Pass/Fail/N/A] | [Link log] | [Môi trường test] | [vX.Y.Z+sha] | [yyyy-mm-dd] | TV1 |
| QA-008 | LoadNextObject trả đúng ObjectID | 1) Chuẩn bị danh sách object test có ObjectID biết trước. 2) Gọi `LoadNextObject`. 3) Đối chiếu ObjectID trả về. | `LoadNextObject` trả về ObjectID khớp mong đợi theo thứ tự xử lý. | [Điền kết quả thực tế] | [Pass/Fail/N/A] | [Link log/screenshot] | [Môi trường test] | [vX.Y.Z+sha] | [yyyy-mm-dd] | TV2 |
| QA-009 | Dashboard hiển thị đúng current state | 1) Chạy PIE và lần lượt kích hoạt các state chính. 2) Quan sát Dashboard widget. 3) Đối chiếu với state backend/log. | Dashboard widget hiển thị đúng state hiện tại theo thời gian thực, không trễ/nhầm state. | [Điền kết quả thực tế] | [Pass/Fail/N/A] | [Link video/screenshot] | [Môi trường test] | [vX.Y.Z+sha] | [yyyy-mm-dd] | TV3 |
| QA-010 | Auto-cycle 3 vòng không crash | 1) Bật chế độ auto-cycle. 2) Chạy liên tục đến hết 3 vòng full pipeline. 3) Theo dõi log và tính ổn định. | Hoàn tất 3 vòng auto-cycle không crash, không memory leak/ngừng đột ngột. | [Điền kết quả thực tế] | [Pass/Fail/N/A] | [Link log/perf capture] | [Môi trường test] | [vX.Y.Z+sha] | [yyyy-mm-dd] | TV4 |

## Glossary (Thuật ngữ)

- **PIE (Play-In-Editor):** Chế độ chạy game trực tiếp trong Unreal Editor để test nhanh.
- **State Transition:** Quá trình chuyển đổi giữa các trạng thái hệ thống (Idle, Scanning, Detected, Error).
- **Evidence:** Bằng chứng xác minh kết quả test (log, screenshot, video, bug ticket).
- **Build/Commit:** Phiên bản build và commit hash ứng với lần test.
- **N/A:** Không áp dụng cho build hiện tại (có lý do rõ ràng).
