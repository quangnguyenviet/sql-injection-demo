@echo off
echo === Django Project Setup and Run Script ===

REM Kiểm tra xem môi trường ảo đã tồn tại chưa
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Kích hoạt môi trường ảo
echo Activating virtual environment...
CALL .\venv\Scripts\activate

REM Cài đặt dependencies
echo Installing dependencies...
pip install django

REM Chạy migrations
echo Running migrations...
python manage.py makemigrations
python manage.py migrate

REM Chạy server
echo Starting Django development server...
python manage.py runserver 8080

REM Giữ cửa sổ mở sau khi chạy xong
pause 