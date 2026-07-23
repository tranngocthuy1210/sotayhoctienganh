# BÀN GIAO DỰ ÁN — Sổ tay học tiếng Anh (web)

> Mở session mới bằng câu: **"Đọc file D:\AI Challenge\so-tay-web\HANDOFF.md rồi làm tiếp phần 'VIỆC TIẾP THEO'."**

Cập nhật: **2026-07-23**. Commit mới nhất: `0c5d3c7`. **Mọi thứ đã đẩy lên, không có việc dở dang.**

---

## 1. DỰ ÁN LÀ GÌ

Web **"SỔ TAY HỌC TIẾNG ANH — by tranngocthuy"**: lộ trình **90 ngày cho người mất gốc**.
Người dùng là **trưởng nhóm kinh doanh phần mềm F&B (iPOS.vn) tại Việt Nam**, bận, ưu tiên **nói + giao tiếp + đàm phán**. Ngữ cảnh xoay quanh POS/KDS/inventory, quản lý nhân sự, đàm phán hợp đồng, IELTS Speaking Part 1.

**⚠️ DỰ ÁN ĐÃ CÓ SẴN — LÀM TIẾP, KHÔNG TẠO MỚI.**

- Repo: https://github.com/tranngocthuy1210/sotayhoctienganh
- **Live: https://sotayhoctienganh.vercel.app** (auto-deploy ~30s khi push)

---

## 2. FILE TRONG DỰ ÁN `D:\AI Challenge\so-tay-web\`

| File | Vai trò | Kích thước |
|---|---|---|
| `index.html` | Toàn bộ web: HTML + CSS + **11 khối JS inline** | ~210KB |
| `data-vocab.js` | Bộ **600 từ** gốc theo chủ đề (12 nhóm), mỗi từ có **1** câu ví dụ | 60KB |
| `data-vocab-plus.js` | **194 từ** mở rộng (3 chủ đề), mỗi từ có **2** câu ví dụ | 29KB |
| `data-vocab-oxford.js` | Kho **Oxford 3000 chia theo 26 CHỦ ĐỀ**: 2649 từ, 2633 có IPA. **CHƯA có ví dụ** | 184KB |
| `data-sentence-vn.js` | **1129 bản dịch tiếng Việt** cho câu chép chính tả | 101KB |
| `data-dictation-tatoeba.js` | **94 câu giọng người thật** (audio Tatoeba, CC BY 4.0) | 7KB |
| `config.js` | Khóa Supabase — ĐÃ ĐIỀN | |
| `manifest.json`, `service-worker.js` | PWA (cache `sotay-v8`) | |
| `SETUP.md` | Hướng dẫn Supabase (PHẦN 1, 1B ghi âm, 1C khoá dữ liệu) | |
| **`tools/`** | **Script dev + cache IPA** — xem mục 6. KHÔNG deploy (có `.vercelignore`) | 1.6MB |

**Tổng kho từ: 3443 từ** (600 + 194 + 2649).

### Supabase — ĐÃ BẬT
Project `so-tay-tieng-anh`, URL `https://lohtwcalxfyflcvpjzwx.supabase.co`, khóa publishable trong `config.js`.
Bảng: `vocab`, `scripts`, `recordings`, `allowed_emails`. Bucket riêng tư `recordings`.
**Đăng nhập**: email magic link, `shouldCreateUser:false`. Chặn người lạ bằng bảng `allowed_emails` + trigger `block_unallowed_signup`.

---

## 3. BỐ CỤC: 6 TAB (sticky dưới header)

1. **Thời khóa biểu** (`#tab-cal`) — lịch 90 ngày + 3 thói quen + báo thức
2. **Sổ tay từ vựng** (`#tab-voc`) — **ô tìm kiếm** + 15 nhóm chủ đề (có ví dụ) + 26 nhóm chủ đề Oxford (tra cứu) + "Của tôi"
3. **Kịch bản đối thoại F&B** (`#tab-script`) — 3 accordion, có tab dọc bên trái
4. **Ghi âm & tiến bộ** (`#tab-rec`) — đăng nhập, thu, nghe lại, so sánh
5. **Ôn từ Anki** (`#tab-anki`) — lặp lại ngắt quãng + chuỗi ngày 🔥
6. **Chép chính tả** (`#tab-dict`) — nghe rồi gõ lại, chấm từng từ

---

## 4. ĐÃ LÀM XONG & ĐÃ CHỐT

| # | Tính năng | Trạng thái |
|---|---|---|
| ➊ | **Nghe phát âm + IPA** — IPA US/UK, nút loa TTS, chọn Mỹ/Anh + Chậm/Thường | ✅ |
| ➋ | **PWA** — manifest, service worker, icon, banner cài | ✅ lõi |
| ➌ | **Ghi âm & tiến bộ** — đăng nhập email, thu, upload Supabase, nghe lại, so sánh | ✅ |
| ➍ | **Ôn từ Anki** — SRS 8 bậc (1→120 ngày), 3 mức chấm, 2 kiểu hỏi Anh→Việt / Việt→Anh, chọn chủ đề, chuỗi ngày 🔥, phím tắt Space/1/2/3 | ✅ |
| ➎ | **Chép chính tả** — nghe (TTS hoặc giọng thật) rồi gõ lại; chấm từng từ bằng LCS, phân biệt sai chính tả / nghe sót / gõ thừa; **hiện nghĩa tiếng Việt của câu đúng**; chuỗi ngày riêng | ✅ |
| ➏ | **Ô tìm kiếm kho từ** — lọc thẳng trong 3443 từ theo từ tiếng Anh **lẫn** nghĩa tiếng Việt, **gõ không dấu vẫn ra** ("hoa don" → bill/invoice/receipt); tô đậm đoạn khớp, hiện tên chủ đề, tối đa 60 kết quả | ✅ |
| — | **Kho từ 3443** — 600 core + 194 mở rộng (2 ví dụ/từ) + 2649 Oxford chia **26 chủ đề** | ✅ |
| — | **IPA đối chiếu Oxford** — toàn bộ, kể cả rà lại bộ 600 gốc (sửa 19 lỗi thật) | ✅ |
| — | **1129 bản dịch tiếng Việt** cho toàn bộ câu chép chính tả | ✅ |
| — | **Giọng người thật** 94 câu Tatoeba CC BY 4.0, có ghi công | ✅ |
| — | **Render lazy** kho từ theo chủ đề (không giật trên mobile) | ✅ |
| — | **Khoá dữ liệu "Của tôi"** theo `user_id` | ✅ code — SQL 1C **có vẻ ĐÃ chạy rồi** (2026-07-23 chạy lại báo `42710: policy "vocab_own" already exists`). **Chờ kết quả `select … from pg_policies` để chốt** |

---

## 5. QUY ƯỚC BẮT BUỘC GIỮ

- **Font: CHỈ `var(--sans)`.** TUYỆT ĐỐI KHÔNG Georgia/serif (vỡ dấu tiếng Việt).
- **Màu:** brand teal `#0F7A6E`; kỹ năng: noi `#4361C9`, nghe `#7A52C4`, doc `#12986E`, viet `#B07D18`, damphan `#C24A66`; gold `#A9790C`. Có dark mode.
- **Icon:** Lucide inline `<symbol>` sprite, KHÔNG load CDN.
- **Ngôn ngữ với người dùng: tiếng Việt**, thẳng thắn, nói rõ đánh đổi.
- Nội dung mới phải **rút gọn cho dễ nói** và **lọc câu trùng lặp**.
- Người dùng **không thích mẫu tin nhắn Zalo** trong web — web này để luyện NÓI.

### ⚠️ BẪY 1: cơ chế `data-ek` (sửa-tay lưu localStorage)
Nội dung sửa-tay lưu với key `"e"+i` **đánh số theo thứ tự xuất hiện** (`HB_SEL` trong khối JS đầu).
**Chèn phần tử khớp `HB_SEL` vào GIỮA trang sẽ làm lệch toàn bộ chữ người dùng đã sửa.**
→ Nội dung mới gắn class **`.nokey`** (HB_SEL có `:not(.nokey)`).
→ Tab mới (Anki, Chép chính tả) dùng **khối HTML rỗng**, toàn bộ UI do JS dựng → không ăn key. **Giữ cách này.**

### ⚠️ BẪY 2: IPA giọng Mỹ — 4 cái bẫy đã gặp
1. **Trang Oxford trả SAI ô "US"** với từ như `nose`, `local`, `shoulder` (để nguyên phiên âm Anh `/nəʊz/`).
   Lỗi hệ thống: trang áp quy tắc Mỹ nhưng bỏ sót phép đổi `əʊ→oʊ`. Đã vá bằng quy tắc.
2. **`ɪə`/`ʊə` là giọng Anh, NHƯNG `aɪə eɪə oʊə aʊə ɔɪə` là giọng Mỹ hợp lệ** mà CHỨA chuỗi con đó
   (fire, player, poem, hour, employer) → phải bỏ các cụm này trước khi kiểm, không thì **xoá oan 52 IPA**.
3. **Từ chức năng → Oxford trả DẠNG YẾU**: `have`→`həv`, `but`→`bət`. Người học cần dạng mạnh → có danh sách loại trừ.
4. **Đồng tự khác trọng âm**: slug `go-ahead`/`hang-up` trả phiên âm DANH TỪ, khác CỤM ĐỘNG TỪ.
   Luôn đối chiếu trường `p` trước khi vá. Tương tự `separate` (v/adj), `transport` (n/v), `download`/`upload`.

### ⚠️ BẪY 3: bản quyền
- **Audio Tatoeba là CC BY 4.0 → BẮT BUỘC ghi công.** Ghi công dồn ở **một khối cuối tab Chép chính tả**
  (`creditHTML()`): Tatoeba + tên người thu + CC BY 4.0. **CẤM bỏ hẳn** — bỏ = vi phạm bản quyền.
  (Người dùng đã yêu cầu bỏ; đã giải thích và dồn xuống cuối thay vì bỏ.)
- Chỉ dùng audio giấy phép **CC BY 4.0 / CC0**. Câu để trống giấy phép thì Tatoeba **CẤM** dùng ngoài.
- **KHÔNG chép câu ví dụ của Oxford** (có bản quyền, khác IPA là dữ liệu sự kiện). Tự viết ví dụ.
- **KHÔNG cắt clip phim/YouTube** như app Parroto — vi phạm bản quyền.

### ⚠️ BẪY 4: chất lượng nguồn mở
Phần audio giấy phép mở của Tatoeba **lệch nặng về câu meme/chính trị/tôn giáo/tục**
("I want some blow", "doggo/pupper", "We have a stegosaurus"). Phải lọc gắt bằng blocklist
+ tỷ lệ từ thông dụng ≥55%, rồi **đọc lại bằng mắt** trước khi đưa vào (đã loại 26 câu ở vòng 2).

### ⚠️ BẪY 5: cache PWA (đã sửa, đừng làm hỏng lại)
Trước đây file `.js` dùng **cache-first** → người dùng thấy bản cũ sau mỗi lần cập nhật dữ liệu,
**đã hiểu nhầm 3 lần** ("sao chỉ có 794 từ"). Đã sửa: `.js/.html/.json` giờ **network-first**
(online luôn mới, offline mới dùng bản lưu); ảnh vẫn cache-first. **Giữ nguyên cách này.**

### ⚠️ BẪY 7: KHÔNG kiểm RLS bằng mã HTTP
Gọi `/rest/v1/vocab` bằng khoá công khai rồi thấy **`200` + `[]`** thì **KHÔNG kết luận được gì**:
bảng đã khoá RLS và bảng rỗng chưa khoá trả về **giống hệt nhau** (PostgREST lọc hết dòng chứ
không trả 401). AI đã kết luận sai đúng chỗ này ngày 2026-07-23 và báo nhầm là "còn lỗ hổng".
**Chỉ kiểm bằng `select … from pg_policies where tablename in ('vocab','scripts')`** — xem PHẦN 1C.

### ⚠️ BẪY 6b: đổi `id` nhóm từ vựng làm hỏng tiến độ Anki
Tab Anki lưu **danh sách chủ đề đã chọn theo `id`** vào localStorage (`ielts90.srs.v1` → `cfg.topics`),
và lưu tiến độ từng thẻ theo khoá `"<id nhóm>|<từ>"`.
Đổi `id` nhóm (như lần bỏ `ox-a…ox-z` sang `ox-work`, `ox-biz`…) sẽ làm bộ lọc khớp **0 chủ đề**
→ tab ôn tập hiện "hết thẻ" một cách vô lý. Đã vá: khi tải lên, lọc bỏ id không còn tồn tại,
sạch hết thì coi như chọn tất cả.
**Đổi `id` nhóm lần nữa thì phải kiểm lại chỗ này** (`onTopic` trong khối JS Anki).
Lưu ý tiến độ thẻ cũ theo id cũ vẫn nằm lại trong localStorage — vô hại nhưng không dùng được nữa.

### ⚠️ BẪY 6: shell làm hỏng regex
Viết script Python bằng **Write tool**, KHÔNG dùng heredoc/inline `python -c` với regex có `\\` —
bash/heredoc nuốt backslash làm regex sai (đã dính nhiều lần).

---

## 6. THƯ MỤC `tools/` — SCRIPT & CACHE (đã kiểm chạy được từ vị trí mới)

Đường dẫn trong script đã sửa thành **tương đối** (`_HERE` = tools/, `_PROJ` = thư mục dự án).
Chạy: `cd "D:\AI Challenge\so-tay-web\tools" && python <script>.py`

### Kiểm tra — LUÔN chạy trước khi đẩy
| Script | Kiểm gì |
|---|---|
| `check.py` | 12 khối JS inline (esprima), cân bằng thẻ HTML, `{`=`}` trong `<style>` |
| `checkvocab.py` | File từ vựng: trùng từ, thiếu trường, IPA sai ký hiệu, ví dụ không chứa từ, ex2 |
| `checkoxford.py` | Kho Oxford: cú pháp JS, trùng từ, trùng id chủ đề, **đối chiếu `.bak` xem có mất từ / lệch IPA-nghĩa không** |
| `testdiff.py` | **20 ca thử thuật toán chấm chính tả** — sửa thuật toán thì PHẢI chạy lại |

### Dựng dữ liệu
| Script | Việc |
|---|---|
| `oxipa.py <file-từ>` | Tra IPA giọng Mỹ từ Oxford (~0.5s/từ, có cache `ox_cache.json`) |
| `ox_extract.py` → `ox_build.py` | Lọc từ Oxford mới → dựng `data-vocab-oxford.js` (**bản A–Z cũ, đã thay**) |
| `ox_topics.py` | **Bảng gán 2649 từ Oxford → 26 chủ đề** (`TOPICS` + `MAP` A–Z). Thêm từ mới thì gán ở đây |
| `ox_regroup.py` | Đọc `data-vocab-oxford.js` → chia lại theo `ox_topics.py`, **giữ nguyên t/ipa/p/vn**. Báo từ chưa gán / từ gán thừa rồi mới ghi file |
| `ox_fixvn.py` | Sửa nghĩa tiếng Việt sai từ bản PDF (đã sửa 8 từ, xem mục 7) |
| `build_vn.py` | Gộp `vn_*.py` → `data-sentence-vn.js`, **kiểm phủ đủ câu** |
| `tatoeba_pick.py` → `tatoeba_clean.py` → `tatoeba_verify.py` | Pipeline lấy câu Tatoeba có audio |
| `tat_clean2.py` | Loại câu rác khỏi bộ Tatoeba |
| `parse3000.py` | Bóc PDF Oxford 3000 → `ox3000_raw.json` |
| `extract_missing.py` | Tìm câu chép chính tả chưa có bản dịch |

### Cache quý — ĐỪNG XOÁ
| File | Nội dung |
|---|---|
| `ox_cache.json` (442KB) | **Kết quả tra ~3400 IPA Oxford** — mất là phải cào lại ~40 phút |
| `ox3000_raw.json` | 3374 từ bóc từ PDF Oxford 3000 |
| `ox_meta.json`, `ox_ipa.json` | Loại từ + nghĩa Việt + IPA đã tra |
| `vn_core.py`, `vn_plus1/2.py`, `vn_scr.py`, `vn_tat.py` | **1129 bản dịch tiếng Việt** (nguồn để thêm batch) |

**Thêm batch bản dịch mới:** viết dict `{en:vn}` vào file `vn_*.py` mới → thêm import vào `build_vn.py` → chạy → đẩy.

---

## 7. VIỆC TIẾP THEO

### 🔴 VIỆC GẤP — người dùng phải tự làm (AI không vào được Supabase dashboard)
**Xác nhận SQL PHẦN 1C đã chạy đủ chưa.** Ngày 2026-07-23 chạy lại thì báo
`42710: policy "vocab_own" for table "vocab" already exists` → **nhiều khả năng đã chạy từ trước**,
mục này trong HANDOFF trước đó ghi sai. Lần chạy lỗi đó đã rollback, không hỏng gì.
Chốt bằng cách chạy query `pg_policies` ở cuối PHẦN 1C trong SETUP.md rồi cập nhật lại mục này.
Khối SQL 1C nay đã **chạy lại được nhiều lần** (thêm `drop policy if exists`).

### 🔴 Ưu tiên cao nhất — RÀ NGHĨA TIẾNG VIỆT KHO OXFORD
Bản PDF Oxford 3000 cho **nghĩa cổ / nghĩa phụ**, sai hẳn với cách dùng hằng ngày.
Đợt 2026-07-23 mới sửa **8 từ** bằng `ox_fixvn.py`:

| Từ | Nghĩa SAI trong PDF | Đã sửa thành |
|---|---|---|
| `staff` | gậy | nhân viên, đội ngũ nhân sự |
| `receipt` | công thức; đơn thuốc | hoá đơn, biên lai |
| `adapt` | lắp vào | thích nghi, điều chỉnh cho phù hợp |
| `order` | thứ, bậc; ra lệnh | đơn hàng, gọi món; ra lệnh; thứ tự |
| `branch` | ngành; nhành cây, ngả đường | chi nhánh, điểm bán |
| `deal` | phân phát, phân phối | thoả thuận, hợp đồng mua bán |
| `quote` | trích dẫn | báo giá; trích dẫn |
| `stock` | sự trữ, vốn | hàng tồn kho; cổ phiếu |

**Còn ~2641 từ CHƯA rà.** 8 lỗi này lòi ra chỉ sau vài phút thử ô tìm kiếm → **tỷ lệ lỗi thật
có thể cao**. Giờ từ đã chia theo chủ đề nên rà theo nhóm nghề nghiệp/kinh doanh trước là hiệu quả nhất.
Cách làm: thêm cặp `từ: nghĩa` vào `FIX` trong `ox_fixvn.py` rồi chạy.

### Ưu tiên cao
1. **Thêm câu ví dụ cho 2649 từ Oxford** — hiện chỉ có từ + IPA + nghĩa + loại từ.
   Đây là hạng mục lớn nhất còn lại. Làm theo đợt như `data-vocab-plus.js` (~250 từ/đợt).
   Giờ đã chia chủ đề nên nên làm **trọn từng chủ đề một** (bắt đầu: Kinh doanh 66 từ, Tiền bạc 46 từ).
2. **Thêm `ex2` cho bộ 600 gốc** — hiện chỉ có 1 câu ví dụ/từ (mã xử lý thiếu ex2 an toàn).
3. **Nhóm `Tính từ mô tả & đánh giá` đang 379 từ, `Suy nghĩ & khái niệm` 251 từ** — hơi to,
   có thể tách nhỏ sau nếu thấy khó học (sửa `TOPICS`+`MAP` trong `ox_topics.py` rồi chạy `ox_regroup.py`).

### Đang treo / chưa làm
- **Thông báo nhắc học 6:30 sáng** — iPhone hạn chế push, cần bàn trước.
- **Bài tập điền khuyết / trắc nghiệm** từ vựng.
- Sao lưu JSON tiến độ.
- Chép chính tả: chưa có chế độ cloze, chưa lưu câu hay sai để ôn lại.
- 2 từ Oxford thiếu IPA (`congratulations`, `groceries`) + các cụm từ ("approve of"…) — Oxford không có mục đơn.
- **Luyện đàm phán với AI** (Claude API) — có phí, cần backend giấu key.
- **Nâng cấp giọng thật**: hiện hotlink audio Tatoeba (không chạy offline). Có thể tải về Supabase Storage.
  Muốn giọng thật đọc **chính câu F&B của bạn** thì phải thuê người bản xứ thu (~100–400$).

---

## 8. QUY TRÌNH KỸ THUẬT

**Máy:** Windows, có **git** + **Python 3.12** (`esprima`, `Pillow`, `requests`, `pypdf`, `cryptography`), KHÔNG có Node/Docker. Git Credential Manager đã lưu GitHub.

**Đẩy lên (đã dùng ~20 lần, chạy tốt):**
```bash
TMP="/tmp/sotay-push-$$"; mkdir -p "$TMP" && cd "$TMP" && \
git clone --depth 1 https://github.com/tranngocthuy1210/sotayhoctienganh repo && \
cd repo && cp "D:/AI Challenge/so-tay-web/index.html" index.html && \
git -c core.safecrlf=false add -A && \
git -c user.name="tranngocthuy1210" -c user.email="tranngocthuy1210@gmail.com" commit -m "..." && \
git push origin HEAD
```
**Copy đủ file đã sửa** (index.html, data-*.js, service-worker.js…). Thông điệp commit **không dấu tiếng Việt**. AI KHÔNG nhập credential.

**Đổi dữ liệu thì nhớ bump `CACHE` trong `service-worker.js`** (hiện `sotay-v8`).

⚠️ **Đẩy 2 lần trong 1 phiên thì coi chừng có 2 thư mục `/tmp/sotay-push-*`** — `ls | head -1`
có thể trỏ nhầm bản clone sạch và báo "nothing to commit". Dùng đường dẫn tường minh.

**✅ KIỂM TRA BẰNG MẮT ĐƯỢC — dùng browser pane với URL https (KHÔNG phải file://):**
```
navigate → https://sotayhoctienganh.vercel.app
javascript_tool → đọc DOM, kiểm giá trị thật
```
Browser pane **chặn `file://` và `localhost`** nhưng **mở được web live**. Đây là cách kiểm chứng
đáng tin nhất — đã dùng để chứng minh dòng ghi công có render, đếm đúng 3443 từ, v.v.
⚠️ Sau khi đẩy phải **tải lại 2 lần** mới qua cache (hoặc thêm `?v=N`).

---

## 9. CÁC MỐC NỘI DUNG (không phá vỡ khi sửa)

- Lịch: **T2 20/07/2026 → CN 11/10/2026**, 84 ngày.
- Ngày 3 (22/07): bản thu tự giới thiệu đầu tiên — để so với Ngày 83.
- Ngày 27, 55, 83: cột mốc. Ngày 84: nghe lại bản 22/07 vs 10/10.
- Tháng 1 nền tảng (Nghe–Nói) · Tháng 2 đủ 4 kỹ năng ngữ cảnh F&B · Tháng 3 IELTS + đàm phán + italki mỗi T7.

---

## 10. LỊCH SỬ COMMIT (2026-07-21 → 23)

```
0c5d3c7 O tim kiem kho tu + chia 2649 tu Oxford theo chu de thay vi A-Z
454b47d Service worker: file .js/.html/.json uu tien mang thay vi cache-first
deeb502 Dich du 1129 cau chep chinh ta + kho Oxford 3000 A-Z that
57ef5ea Chep chinh ta: hien nghia tieng Viet cua cau dung (batch 1: 600 cau core)
34fc1da Chep chinh ta: bo nhan 'giong nguoi that' bi lap tren the
cf86bd4 Chep chinh ta: don ghi cong Tatoeba xuong cuoi tab
3422a5c Chep chinh ta: them nguon Giong nguoi that tu Tatoeba
33cecd1 Them tab Chep chinh ta (dictation)
68abe4d Moi tu co 2 cau vi du: viec cua ban + ngu canh khac
10a7642 Them tab On tu Anki (spaced repetition + chuoi ngay), mo rong kho tu vung
```
