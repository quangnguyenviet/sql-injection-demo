from django.shortcuts import render
from django.db import connection

def login_view(request):
    
    message = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # ❌ Cố tình không an toàn để demo SQL Injection
        with connection.cursor() as cursor:
            query = f"SELECT * FROM loginapp_user WHERE username = '{username}' AND password = '{password}'"
            cursor.execute(query)
            user = cursor.fetchone()

        if user:
            message = "Đăng nhập thành công!"
        else:
            message = "Sai tài khoản hoặc mật khẩu."

    return render(request, 'login.html', {'message': message})

def register_view(request):
    message = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # ❌ Cố tình không an toàn để minh hoạ SQL Injection
        with connection.cursor() as cursor:
            # try:
            #     query = f"INSERT INTO loginapp_user (username, password) VALUES ('{username}', '{password}')"
            #     cursor.execute(query)
            #     message = "Đăng ký thành công!"
            # except Exception as e:
            #     message = f"Lỗi: {str(e)}"
                
            query = f"INSERT INTO loginapp_user (username, password) VALUES ('{username}', '{password}')"
            cursor.execute(query)
            message = "Đăng ký thành công!"

    return render(request, 'register.html', {'message': message})

def update_password_view(request):
    message = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')

        # ❌ Không an toàn, dễ bị SQL Injection
        with connection.cursor() as cursor:
            try:
                query = f"UPDATE loginapp_user SET password = '{new_password}' WHERE username = '{username}'"
                cursor.execute(query)
                message = "Cập nhật mật khẩu thành công!"
            except Exception as e:
                message = f"Lỗi: {str(e)}"

    return render(request, 'updatePassword.html', {'message': message})

