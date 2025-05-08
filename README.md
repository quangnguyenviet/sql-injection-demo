# Django SQL Injection Demo Project

Dự án này là một ví dụ để minh họa các lỗ hổng **SQL Injection** trong ứng dụng Django. **Không an toàn** và chỉ dùng để học tập hoặc kiểm thử trong môi trường được kiểm soát.

---

## 📦 Yêu cầu

- Python 3.8 trở lên
- Git (nếu bạn clone từ repository)
- Windows (để chạy `run_django.bat`)

---

## 🚀 Khởi chạy dự án

### 1. Clone repository (nếu cần)

```bash
git clone <URL repository>
cd sql-injection-demo
```

### 2. Chạy file `run_django.bat`

Click đúp hoặc chạy trong terminal:

```bash
./run_django.bat
```

Tập lệnh sẽ:
- Tạo môi trường ảo nếu chưa có (`venv`)
- Kích hoạt môi trường ảo
- Cài đặt Django
- Chạy `makemigrations` và `migrate`
- Khởi động server tại [http://127.0.0.1:8080](http://127.0.0.1:8080)

---

## 🌱 Tạo dữ liệu mẫu

Sau khi server khởi chạy, để thêm dữ liệu mẫu:

### Bước 1: Kích hoạt môi trường ảo

```bash
venv\Scripts\activate
```

(hoặc với PowerShell: `venv\Scripts\Activate.ps1`)

### Bước 2: Chạy script

```bash
python seed_data.py
```

---

## 📂 Cấu trúc dự án

```
├── loginapp/             # App Django chính
├── sql_inject_demo/      # Cấu hình project Django
├── templates/            # Giao diện HTML
├── db.sqlite3            # SQLite database
├── seed_data.py          # Tạo dữ liệu mẫu (người dùng, sản phẩm, v.v.)
├── run_django.bat        # Tự động setup và chạy server
├── manage.py
```

---

## ✅ Tài khoản mẫu

```text
Username: admin
Password: admin123
```

Sau khi đăng nhập bằng tài khoản admin, bạn sẽ được chuyển đến trang tìm kiếm người dùng.

---

## ⚠️ Cảnh báo bảo mật

**Dự án này chứa các lỗi bảo mật nghiêm trọng**:
- SQL Injection
- Không dùng các phương thức xác thực Django chuẩn
- Lưu mật khẩu dưới dạng plaintext

⚠️ **Không triển khai dự án này trên môi trường thực tế.** Chỉ dùng cho mục đích học tập hoặc mô phỏng kiểm thử bảo mật.

---

## 📞 Liên hệ

Nếu bạn có thắc mắc hoặc muốn đóng góp, hãy liên hệ với nhóm phát triển hoặc giảng viên hướng dẫn của bạn.