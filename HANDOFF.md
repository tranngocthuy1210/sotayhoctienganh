# BÀN GIAO DỰ ÁN — Sổ tay học tiếng Anh (web)

> Mở session mới bằng câu: **"Đọc file D:\AI Challenge\so-tay-web\HANDOFF.md rồi làm tiếp phần 'VIỆC TIẾP THEO'."**

Cập nhật: **2026-07-19**. Commit mới nhất: `e111ea5`.

---

## 1. DỰ ÁN LÀ GÌ

Web **"SỔ TAY HỌC TIẾNG ANH — by tranngocthuy"**: lộ trình **90 ngày cho người mất gốc**.
Người dùng là **trưởng nhóm kinh doanh phần mềm F&B (iPOS.vn) tại Việt Nam**, bận, ưu tiên **nói + giao tiếp + đàm phán**. Ngữ cảnh xoay quanh POS/KDS/inventory, quản lý nhân sự, đàm phán hợp đồng, IELTS Speaking Part 1.

**⚠️ DỰ ÁN ĐÃ CÓ SẴN — LÀM TIẾP, KHÔNG TẠO MỚI.**

---

## 2. HIỆN TRẠNG

### File mã nguồn: `D:\AI Challenge\so-tay-web\`
| File | Vai trò |
|---|---|
| `index.html` | Toàn bộ web (~1800 dòng): HTML + CSS + 8 khối JS inline |
| `data-vocab.js` | Bộ **600 từ**, 12 chủ đề × 50 (t/ipa/p/vn/ex/tip) |
| `config.js` | Khóa Supabase — **ĐÃ ĐIỀN** |
| `manifest.json`, `service-worker.js` | PWA |
| `icon-192/512/maskable-512.png`, `apple-touch-icon.png` | Icon (vẽ bằng Pillow, script trong lịch sử chat) |
| `SETUP.md` | Hướng dẫn Supabase (PHẦN 1, 1B ghi âm, 1C khoá dữ liệu) |

### Đã lên mạng
- Repo: https://github.com/tranngocthuy1210/sotayhoctienganh
- **Live: https://sotayhoctienganh.vercel.app** (auto-deploy ~30s khi push)
- GitHub Pages: https://tranngocthuy1210.github.io/sotayhoctienganh/

### Supabase — ĐÃ BẬT
- Project `so-tay-tieng-anh`, URL `https://lohtwcalxfyflcvpjzwx.supabase.co`, khóa publishable trong `config.js`.
- Bảng: `vocab`, `scripts`, `recordings`, `allowed_emails`. Bucket riêng tư `recordings`.
- **Đăng nhập**: email magic link, `shouldCreateUser:false`. Chặn người lạ bằng bảng `allowed_emails` + trigger `block_unallowed_signup` trên `auth.users`.

### Bố cục: 4 TAB ở đầu trang (sticky dưới header)
1. **Thời khóa biểu** (`#tab-cal`) — lịch 90 ngày + thẻ 3 thói quen + báo thức + nút "Về đầu trang"
2. **Sổ tay từ vựng** (`#tab-voc`) — 600 từ theo chủ đề + Tuần 5–8 + "Của tôi"
3. **Kịch bản đối thoại F&B** (`#tab-script`) — 3 accordion, mỗi cái có **tab dọc bên trái**
4. **Ghi âm & tiến bộ** (`#tab-rec`) — đăng nhập, thu, nghe lại, so sánh

---

## 3. QUY ƯỚC THIẾT KẾ (BẮT BUỘC GIỮ)

- **Font: CHỈ `var(--sans)`.** TUYỆT ĐỐI KHÔNG Georgia/serif (vỡ dấu tiếng Việt). Đã rà: 92/92 khai báo đúng.
- **Màu:** brand teal `#0F7A6E`; kỹ năng: noi `#4361C9`, nghe `#7A52C4`, doc `#12986E`, viet `#B07D18`, damphan `#C24A66`; gold `#A9790C`. Có dark mode.
- **Icon:** Lucide inline `<symbol>` sprite, KHÔNG load CDN.
- **Ngôn ngữ với người dùng: tiếng Việt**, thẳng thắn, nói rõ đánh đổi.
- **Nội dung mới thêm phải rút gọn cho dễ nói** (người mất gốc) và **lọc câu trùng lặp** — người dùng đã yêu cầu 3 lần.
- Người dùng **không thích mẫu tin nhắn Zalo** trong web (đã bỏ 2 lần) — web này để luyện NÓI.

### ⚠️ BẪY QUAN TRỌNG NHẤT: cơ chế `data-ek`
Nội dung sửa-tay trên trang lưu vào localStorage với key `"e"+i` **đánh số theo thứ tự xuất hiện** (`HB_SEL` trong khối JS đầu).
**Chèn phần tử khớp `HB_SEL` vào GIỮA trang sẽ làm lệch toàn bộ chữ người dùng đã sửa.**
→ Giải pháp đang dùng: nội dung mới gắn class **`.nokey`** (HB_SEL có `:not(.nokey)`). Hiện có 42 phần tử "cũ" giữ key, ~51 phần tử mới `.nokey`.
→ Mọi thao tác **sắp xếp lại DOM** (như tab dọc) phải chạy **SAU** khối JS đầu — key nằm trên thuộc tính nên đi theo phần tử khi di chuyển.

---

## 4. ĐÃ LÀM XONG

| # | Tính năng | Trạng thái |
|---|---|---|
| ➊ | **Nghe phát âm + IPA** — IPA soạn tay US/UK, nút loa TTS, chọn Mỹ/Anh + Chậm/Thường | ✅ |
| ➋ | **PWA** — manifest, service worker (offline + tự cập nhật), icon, banner cài | ✅ lõi |
| ➌ | **Ghi âm & tiến bộ** — đăng nhập email, thu (MediaRecorder ~32kbps), upload Supabase Storage, nghe lại, so sánh 2 bản | ✅ |
| — | **Bộ 600 từ** 12 chủ đề, mỗi từ IPA(Mỹ) + loa + nghĩa + ví dụ + mẹo | ✅ |
| — | **Gộp 4 tab** + thanh tab sticky + tối ưu mobile | ✅ |
| — | **Nút "Thu âm" trên 34/84 thẻ ngày** có bài NÓI | ✅ |
| — | **Tab dọc** cho các khối kịch bản (Tháng 3: 25 mục → 4 tab) | ✅ |
| — | **Khoá dữ liệu "Của tôi"** theo `user_id` | ✅ code — **CHỜ USER CHẠY SQL PHẦN 1C** |

### Nội dung kịch bản đã bổ sung (đều `.nokey`)
- **Tháng 2**: khối "Giới thiệu công ty 10 giây" — 2 nhóm (Ngắn gọn / Mở đầu tư vấn), 4 câu.
- **Ngày 61 Discovery**: mẫu mở & chốt, 12 câu hỏi (nhóm A–D), 3 hội thoại mẫu.
- **Ngày 68 Báo giá**: 6 từ khoá có IPA, cơ cấu 3 phần, phí khởi tạo vs thuê bao, xử lý giá cao, chốt mềm.
- **Ngày 75 Phản đối**: khung 4 bước, mẫu "tách nhỏ chi phí", 6 từ khoá.
- **Ngày 82 Chốt**: mở lời xác nhận (có câu "ai ký / ai thanh toán"), 4 ý bắt buộc, 2 mẫu chốt, 4 từ khoá.

---

## 5. VIỆC TIẾP THEO

### 🔴 VIỆC GẤP — người dùng phải tự làm
**Chạy SQL PHẦN 1C trong SETUP.md** (Supabase → SQL Editor) để khoá `vocab`/`scripts` theo `user_id`.
Chưa chạy thì **ai có link vẫn sửa/xoá được** từ vựng & kịch bản "Của tôi" (code đã sẵn sàng, chỉ chờ đổi chính sách RLS).

### Chưa làm / đang treo
- **Thông báo nhắc học 6:30 sáng** (phần còn lại của ➋). Đã hoãn: iPhone hạn chế push, cần bàn trước.
- **Bài tập điền khuyết / trắc nghiệm** từ vựng — người dùng có gợi ý, chưa làm.
- Ôn từ kiểu Anki (spaced repetition), chuỗi ngày 🔥, ô tìm kiếm, sao lưu JSON.
- Luyện đàm phán với AI (Claude API) — **có phí**, cần backend giấu key.

---

## 6. QUY TRÌNH KỸ THUẬT

**Máy:** Windows, có **git** + **Python 3.12 (có `esprima`, `Pillow`)**, KHÔNG có Node/Docker. Git Credential Manager đã lưu GitHub.

**Đẩy lên (đã dùng ~15 lần, chạy tốt):**
```bash
TMP="/tmp/sotay-push-$$"; mkdir -p "$TMP" && cd "$TMP" && \
git clone --depth 1 https://github.com/tranngocthuy1210/sotayhoctienganh repo && \
cd repo && cp "D:/AI Challenge/so-tay-web/index.html" index.html && \
git -c core.safecrlf=false add -A && \
git -c user.name="tranngocthuy1210" -c user.email="tranngocthuy1210@gmail.com" commit -m "..." && \
git push origin HEAD
```
Thông điệp commit **không dấu tiếng Việt**. AI KHÔNG nhập credential.

**Kiểm tra trước khi đẩy (LUÔN chạy):** Python + `esprima.parseModule` cho từng khối `<script>` inline, `html.parser` đếm cân đối thẻ, và đếm `{` = `}` trong `<style>`.

**⚠️ Giới hạn môi trường:** Browser pane **chặn `file://` và `localhost`** → AI **không tự render kiểm tra bằng mắt được**. Luôn nhờ người dùng mở web thật + Ctrl+F5 + chụp màn hình.

---

## 7. CÁC MỐC NỘI DUNG (không phá vỡ khi sửa)

- Lịch: **T2 20/07/2026 → CN 11/10/2026**, 84 ngày.
- Ngày 3 (22/07): bản thu tự giới thiệu đầu tiên — để so với Ngày 83.
- Ngày 27, 55, 83: cột mốc. Ngày 84: nghe lại bản 22/07 vs 10/10.
- Tháng 1 nền tảng (Nghe–Nói) · Tháng 2 đủ 4 kỹ năng ngữ cảnh F&B · Tháng 3 IELTS + đàm phán + italki mỗi T7.
