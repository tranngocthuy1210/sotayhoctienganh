# SỔ TAY HỌC TIẾNG ANH — Hướng dẫn đưa lên web thật

Bộ này gồm 3 file, tất cả nằm trong thư mục `so-tay-web`:

| File | Vai trò |
|---|---|
| `index.html` | Toàn bộ trang web (lịch + sổ tay). Không cần build, không cần cài gì. |
| `config.js` | Nơi bạn dán 2 khóa Supabase để bật đồng bộ đám mây. |
| `SETUP.md` | File hướng dẫn này. |

> **Mẹo:** Bạn có thể nháy đúp `index.html` để mở thử ngay bây giờ. Khi chưa cấu hình Supabase, mọi thứ vẫn chạy — phần "Của tôi" sẽ lưu tạm trên máy này (huy hiệu vàng "Lưu tại máy này").

---

## PHẦN 1 — Bật đồng bộ đám mây với Supabase (miễn phí)

### Bước 1. Tạo dự án Supabase
1. Vào **https://supabase.com** → **Start your project** → đăng nhập bằng GitHub hoặc email.
2. Bấm **New project**. Đặt tên bất kỳ (vd: `so-tay-tieng-anh`), đặt mật khẩu database (lưu lại), chọn region gần (Singapore).
3. Chờ ~1–2 phút cho dự án khởi tạo.

### Bước 2. Tạo 2 bảng dữ liệu
1. Menu trái → **SQL Editor** → **New query**.
2. Dán toàn bộ đoạn dưới đây rồi bấm **Run**:

```sql
create table if not exists vocab (
  id uuid primary key default gen_random_uuid(),
  group_name text default '',
  term text not null,
  ipa text default '',
  meaning text default '',
  note text default '',
  created_at timestamptz default now()
);
-- Nếu bảng vocab đã tạo TRƯỚC khi có tính năng IPA, chạy thêm dòng này 1 lần:
-- alter table vocab add column if not exists ipa text default '';

create table if not exists scripts (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  body text default '',
  created_at timestamptz default now()
);

alter table vocab   enable row level security;
alter table scripts enable row level security;

create policy "cho phep doc ghi vocab"   on vocab   for all using (true) with check (true);
create policy "cho phep doc ghi scripts" on scripts for all using (true) with check (true);
```

### Bước 3. Lấy 2 khóa
1. Menu trái → **Project Settings** (bánh răng) → **API**.
2. Copy 2 giá trị:
   - **Project URL** → dán vào `SB_URL`.
   - **Project API keys → anon / public** → dán vào `SB_KEY`.
3. Mở file `config.js`, điền vào, lưu lại. Ví dụ:

```js
window.SB_URL = "https://abcdxyzptuv.supabase.co";
window.SB_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6...";  // chuỗi rất dài
```

Xong! Mở lại `index.html`, huy hiệu ở khu "Của tôi" chuyển sang xanh **"Đồng bộ đám mây"**. Giờ thêm ở máy tính thì điện thoại cũng thấy (và ngược lại).

> **Về bảo mật:** anon key vốn được thiết kế để công khai. Với thiết lập trên, bất kỳ ai biết địa chỉ web của bạn đều có thể thêm/sửa/xoá từ vựng & kịch bản. Vì đây là sổ tay cá nhân thì thường không sao. Nếu muốn khoá lại (chỉ mình bạn sửa được), nhắn mình thêm phần đăng nhập — cần vài bước nữa.

---

## PHẦN 1B — Bật GHI ÂM lưu cloud (có đăng nhập) — cho tính năng ➌

Để ghi âm bài nói, lưu lên đám mây và nghe lại trên mọi thiết bị (kể cả so sánh Ngày 3 ↔ Ngày 83), làm thêm 3 việc trong Supabase (vẫn miễn phí, gói free 1 GB — thừa cho hàng ngàn bản thu giọng nói).

> Ghi âm KHÔNG lưu vào GitHub. GitHub chỉ chứa mã nguồn. File âm thanh nằm trong Supabase Storage của bạn.

### Bước A. Tạo bảng + kho chứa file + phân quyền (SQL)
SQL Editor → New query → dán đoạn dưới → **Run**:

```sql
-- Bảng ghi thông tin từng bản thu (không chứa file, chỉ metadata)
create table if not exists recordings (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  day int,                 -- ngày trong lộ trình (vd 3, 83), có thể để trống
  label text default '',   -- nhãn tự do (vd "Tự giới thiệu")
  path text not null,      -- đường dẫn file trong kho
  duration real default 0, -- độ dài (giây)
  created_at timestamptz default now()
);
alter table recordings enable row level security;
create policy "rec_select_own" on recordings for select using (auth.uid() = user_id);
create policy "rec_insert_own" on recordings for insert with check (auth.uid() = user_id);
create policy "rec_delete_own" on recordings for delete using (auth.uid() = user_id);

-- Kho chứa file âm thanh, để RIÊNG TƯ (không public)
insert into storage.buckets (id, name, public) values ('recordings','recordings', false)
on conflict (id) do nothing;

-- Chỉ chủ sở hữu mới đọc/ghi/xoá file trong thư mục mang tên user_id của họ
create policy "rec_files_select" on storage.objects for select
  using (bucket_id='recordings' and auth.uid()::text = (storage.foldername(name))[1]);
create policy "rec_files_insert" on storage.objects for insert
  with check (bucket_id='recordings' and auth.uid()::text = (storage.foldername(name))[1]);
create policy "rec_files_delete" on storage.objects for delete
  using (bucket_id='recordings' and auth.uid()::text = (storage.foldername(name))[1]);
```

### Bước B. Bật đăng nhập bằng email (magic link)
1. Menu trái → **Authentication** → **Providers** → **Email**: để **bật** (mặc định đã bật). Có thể **TẮT** "Confirm email" cho đỡ 1 bước xác nhận.
2. **Authentication** → **URL Configuration**:
   - **Site URL**: `https://sotayhoctienganh.vercel.app`
   - **Redirect URLs** → Add: `https://sotayhoctienganh.vercel.app/` và `https://tranngocthuy1210.github.io/sotayhoctienganh/`
3. (Không cần đổi gì thêm — người dùng nhập email, nhận link đăng nhập trong hộp thư, bấm là vào.)

### Bước C. Dán khóa vào config.js
Giống PHẦN 1 (URL + anon key). Nếu đã làm PHẦN 1 rồi thì **không cần làm lại** — dùng chung 1 dự án Supabase.

Xong 3 bước trên, báo mình (hoặc commit `config.js` đã điền khóa) — mình sẽ bật khu **"Ghi âm & tiến bộ"**: nút thu trong các ngày có bài NÓI, nghe lại, và màn hình so sánh mốc đầu ↔ cuối.

> **Bảo mật:** file để bucket riêng tư + phân quyền theo `user_id`, nên **chỉ bạn (sau khi đăng nhập email của bạn)** mới nghe/tải được bản thu của mình. Người khác có link web cũng không truy cập được file.

---

## PHẦN 2 — Đăng lên GitHub Pages (miễn phí, tên miền `tranngocthuy.github.io`)

### Bước 1. Tạo tài khoản & kho chứa (repository)
1. Vào **https://github.com** → đăng ký (nếu chưa có). Tên đăng nhập bạn chọn sẽ thành tên miền, vd `tranngocthuy`.
2. Bấm **New repository**. Đặt tên vd `so-tay-tieng-anh`. Chọn **Public**. Bấm **Create repository**.

### Bước 2. Tải 3 file lên
1. Trong repo vừa tạo → bấm **Add file → Upload files**.
2. Kéo cả 3 file (`index.html`, `config.js`, `SETUP.md`) vào.
3. Bấm **Commit changes**.

### Bước 3. Bật GitHub Pages
1. Trong repo → **Settings** → menu trái **Pages**.
2. Mục **Source**: chọn **Deploy from a branch**.
3. **Branch**: chọn `main`, thư mục `/ (root)` → **Save**.
4. Chờ ~1 phút. Tải lại trang Pages, sẽ hiện link kiểu:

   **https://tranngocthuy.github.io/so-tay-tieng-anh/**

Đó là web thật của bạn. Gửi link đó cho ai cũng mở được.

### Cập nhật sau này
Sửa nội dung trực tiếp trên web (từ vựng/kịch bản/tick) thì tự lưu — không cần đụng GitHub.
Chỉ khi muốn đổi giao diện / cấu trúc mới cần sửa lại `index.html` trên GitHub (**Add file → Upload files**, ghi đè file cũ).

---

## Câu hỏi thường gặp

**Không điền Supabase có sao không?** Không sao — web vẫn chạy, chỉ là nội dung "Của tôi" lưu riêng từng máy, không đồng bộ.

**Tick lịch và chữ sửa trong ô lịch có đồng bộ không?** Chưa — hiện chỉ phần "Của tôi" (từ vựng & kịch bản bạn tự thêm) đồng bộ qua Supabase. Tick và sửa ô lịch vẫn lưu theo từng máy. Muốn đồng bộ luôn phần đó thì nhắn mình.

**Có tốn tiền không?** Không. Cả Supabase (gói free) và GitHub Pages đều miễn phí cho nhu cầu cá nhân.
