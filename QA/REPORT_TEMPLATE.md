# Báo cáo tiến độ - Tuần [N]

> Mục tiêu: Tổng hợp tiến độ, chất lượng test, rủi ro và quyết định release theo từng buổi/chu kỳ.
>
> Hướng dẫn nhanh cho thành viên mới:
> 1) Điền thông tin Build đầu tiên.
> 2) Cập nhật Scope + Progress theo feature và theo TV.
> 3) Đối chiếu kết quả test với `QA_CHECKLIST_PIE.md` (cùng ID QA-001 -> QA-010).
> 4) Đánh dấu Exit Criteria để chốt hướng đi tiếp theo.

## 1. Build Information

| Trường thông tin | Giá trị |
| --- | --- |
| Version | [VD: v0.3.2] |
| Commit | [VD: a1b2c3d] |
| Ngày báo cáo | [yyyy-mm-dd] |
| Môi trường test | [VD: Win11 + UE5.4 + RTX3060 + PIE] |

## 2. Scope & Definition of Done

| Feature | Owner | Tiêu chí hoàn thành (Definition of Done) | Trạng thái | % Complete |
| --- | --- | --- | --- | --- |
| [Feature 1] | [TVx] | [Mô tả tiêu chí hoàn thành] | [Not started/In progress/Done] | [0-100%] |
| [Feature 2] | [TVx] | [Mô tả tiêu chí hoàn thành] | [Not started/In progress/Done] | [0-100%] |
| [Feature 3] | [TVx] | [Mô tả tiêu chí hoàn thành] | [Not started/In progress/Done] | [0-100%] |

## 3. Progress

### 3.1 Theo thành viên (TV)

| TV | Công việc đã hoàn thành | Công việc tồn đọng | Blocker hiện tại | % Complete |
| --- | --- | --- | --- | --- |
| TV1 | [Đã hoàn thành ...] | [Còn tồn đọng ...] | [Nếu có] | [0-100%] |
| TV2 | [Đã hoàn thành ...] | [Còn tồn đọng ...] | [Nếu có] | [0-100%] |
| TV3 | [Đã hoàn thành ...] | [Còn tồn đọng ...] | [Nếu có] | [0-100%] |
| TV4 | [Đã hoàn thành ...] | [Còn tồn đọng ...] | [Nếu có] | [0-100%] |
| TV5 | [Đã hoàn thành ...] | [Còn tồn đọng ...] | [Nếu có] | [0-100%] |
| TV6 | [Đã hoàn thành ...] | [Còn tồn đọng ...] | [Nếu có] | [0-100%] |

### 3.2 Theo feature/module

| Feature/Module | Tiến độ hiện tại | % Complete | Ghi chú |
| --- | --- | --- | --- |
| [Feature 1] | [Đúng kế hoạch/Chậm] | [0-100%] | [Nếu có] |
| [Feature 2] | [Đúng kế hoạch/Chậm] | [0-100%] | [Nếu có] |
| [Feature 3] | [Đúng kế hoạch/Chậm] | [0-100%] | [Nếu có] |

## 4. Blockers & Risks

| Mức độ (High/Medium/Low) | Mô tả blocker/risk | Owner | Mitigation (hướng giải quyết) | Current Status | Deadline giải quyết |
| --- | --- | --- | --- | --- | --- |
| [High/Medium/Low] | [Mô tả blocker/risk] | [TVx] | [Hành động giảm thiểu/rút gọn rủi ro] | [Open/In progress/Resolved] | [yyyy-mm-dd] |
| [High/Medium/Low] | [Mô tả blocker/risk] | [TVx] | [Hành động giảm thiểu/rút gọn rủi ro] | [Open/In progress/Resolved] | [yyyy-mm-dd] |
| [High/Medium/Low] | [Mô tả blocker/risk] | [TVx] | [Hành động giảm thiểu/rút gọn rủi ro] | [Open/In progress/Resolved] | [yyyy-mm-dd] |

## 5. Demo Checklist (Liên kết QA Checklist)

> Lưu ý: Danh sách dưới đây phải trùng trạng thái với các dòng tương ứng trong `QA_CHECKLIST_PIE.md`.
> Nếu mục nào `Fail`, bắt buộc điền `Evidence` và mã ticket bug trong file checklist QA.

- [ ] QA-001 - Scene load không crash
- [ ] QA-002 - FPS idle > 60
- [ ] QA-003 - StateManager initialized log
- [ ] QA-004 - Trigger Idle -> Scanning
- [ ] QA-005 - Trigger Scanning -> Detected
- [ ] QA-006 - Trigger transition sang Error
- [ ] QA-007 - DataTable load 20 rows
- [ ] QA-008 - LoadNextObject trả đúng ObjectID
- [ ] QA-009 - Dashboard hiển thị đúng current state
- [ ] QA-010 - Auto-cycle 3 vòng không crash

## 6. Kế hoạch buổi tiếp theo

| TV | Priority task | Expected output | Hỗ trợ cần thiết |
| --- | --- | --- | --- |
| TV1 | [Task ưu tiên] | [Kết quả kỳ vọng] | [Người/nguồn lực cần hỗ trợ] |
| TV2 | [Task ưu tiên] | [Kết quả kỳ vọng] | [Người/nguồn lực cần hỗ trợ] |
| TV3 | [Task ưu tiên] | [Kết quả kỳ vọng] | [Người/nguồn lực cần hỗ trợ] |
| TV4 | [Task ưu tiên] | [Kết quả kỳ vọng] | [Người/nguồn lực cần hỗ trợ] |
| TV5 | [Task ưu tiên] | [Kết quả kỳ vọng] | [Người/nguồn lực cần hỗ trợ] |
| TV6 | [Task ưu tiên] | [Kết quả kỳ vọng] | [Người/nguồn lực cần hỗ trợ] |

## 7. Exit Criteria

> Chọn 1 trạng thái cuối cùng cho buổi/chu kỳ và ghi rõ lý do.

- [ ] **Release** - Đạt chất lượng để demo/release (tất cả mục critical đã Pass, không còn blocker High mở).
- [ ] **Continue** - Cần tiếp tục phát triển/test thêm (còn tồn tại mục Medium/Low hoặc task đang dang dở).
- [ ] **Block** - Tạm dừng release do blocker nghiêm trọng (còn High risk chưa có mitigation khả thi).

**Lý do quyết định:** [Tóm tắt 2-3 câu về căn cứ ra quyết định]
