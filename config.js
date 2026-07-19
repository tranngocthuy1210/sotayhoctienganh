/* =========================================================================
   CẤU HÌNH ĐỒNG BỘ ĐÁM MÂY (Supabase)
   -------------------------------------------------------------------------
   - Khóa "publishable" (hoặc anon) được thiết kế để CÔNG KHAI trong web.
     An toàn vì dữ liệu đã khoá bằng Row Level Security + danh sách email
     được phép đăng nhập (xem SETUP.md → PHẦN 1B).
   - TUYỆT ĐỐI KHÔNG dán khóa service_role / secret vào đây.
   - Để trống 2 dòng dưới thì web vẫn chạy, chỉ là lưu tại máy này.
   ========================================================================= */

window.SB_URL = "https://lohtwcalxfyflcvpjzwx.supabase.co";
window.SB_KEY = "sb_publishable_jR1VliEaSpBib4vGRaIcuQ_i-XAiaEc";
