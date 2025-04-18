from django.shortcuts import render
from django.db import connection
from .models import Product
from django.db.models import Q


def login_view(request):
    
    message = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        with connection.cursor() as cursor:
            query = f"SELECT * FROM loginapp_user WHERE username = '{username}' AND password = '{password}'"
            cursor.execute(query)
            row = cursor.fetchone()

            if row:
                # Sử dụng hàm chuyển đổi để lấy dữ liệu dưới dạng dictionary
                user = tuple_to_dict(cursor, row)
                message = f"Đăng nhập thành công! Xin chào, {user['username']}."
            else:
                message = "Sai tài khoản hoặc mật khẩu."



    return render(request, 'login.html', {'message': message})
# ' or 1 = 1;--


def register_view(request):
    message = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # ❌ Cố tình không an toàn để minh hoạ SQL Injection
        with connection.cursor() as cursor:
            query = f"INSERT INTO loginapp_user (username, password) VALUES ('{username}', '{password}')"
            cursor.execute(query)
            message = "Đăng ký thành công!"
    return render(request, 'register.html', {'message': message})

# admin', 'newpass') ON CONFLICT(username) DO UPDATE SET password = 'newpass';

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


def search(request):
    keyword = request.GET.get('q')
    cursor = connection.cursor()
    query = f"SELECT username FROM loginapp_user WHERE username LIKE '%{keyword}%'"
    cursor.execute(query)
    rows = cursor.fetchall()

    # Chuyển đổi từng kết quả thành dictionary
    results = [tuple_to_dict(cursor, row) for row in rows]

    return render(request, 'search.html', {'results': results})

# %' UNION SELECT CONCAT_WS(', ', password, username) as username FROM loginapp_user --


# def product_search(request):
#     query = request.GET.get('q')
#     results = []
#     if query:
#         results = Product.objects.filter(
#             Q(name__icontains=query) | Q(description__icontains=query)
#         )
#     context = {'query': query, 'results': results}
#     return render(request, 'product_search.html', context)


def product_search(request):
    query = request.GET.get('q')
    results = []

    if query:
        cursor = connection.cursor()
        # Sử dụng parameterized query để tránh SQL Injection
        sql = """
            SELECT * FROM loginapp_product
            WHERE name LIKE %s OR description LIKE %s
        """
        like_pattern = f"%{query}%"
        cursor.execute(sql, [like_pattern, like_pattern])
        rows = cursor.fetchall()
        results = [tuple_to_dict(cursor, row) for row in rows]

    context = {'query': query, 'results': results}
    return render(request, 'product_search.html', context)


def tuple_to_dict(cursor, row):
    """
    Chuyển đổi kết quả từ tuple thành dictionary với tên cột làm khóa.
    """
    return {column[0]: value for column, value in zip(cursor.description, row)}


