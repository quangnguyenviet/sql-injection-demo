import os
import django
from django.core.files import File
from pathlib import Path
import requests
from PIL import Image
from io import BytesIO
import time

# Thiết lập môi trường Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sql_inject_demo.settings')
django.setup()

from loginapp.models import User, Product, Category

def download_image(url, retries=3, delay=1):
    """
    Tải ảnh từ URL với retry và delay
    """
    for i in range(retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Kiểm tra status code
            img_data = BytesIO(response.content)
            img = Image.open(img_data)
            return img
        except Exception as e:
            print(f"Lần {i+1}: Không thể tải ảnh từ {url}. Lỗi: {str(e)}")
            if i < retries - 1:  # Nếu còn lần retry
                time.sleep(delay)  # Đợi trước khi thử lại
    return None

def create_sample_data():
    """
    Tạo dữ liệu mẫu cho cơ sở dữ liệu.
    """
    # Tạo users
    users = [
        {'username': 'admin', 'password': 'admin123'},
        {'username': 'user1', 'password': 'password123'},
        {'username': 'user2', 'password': 'password123'},
        {'username': 'test', 'password': 'test123'},
        {'username': 'john_doe', 'password': 'john123'},
        {'username': 'jane_smith', 'password': 'jane123'},
        {'username': 'bob_wilson', 'password': 'bob123'},
        {'username': 'alice_brown', 'password': 'alice123'},
        {'username': 'mike_jones', 'password': 'mike123'},
        {'username': 'sarah_davis', 'password': 'sarah123'}
    ]
    
    for user_data in users:
        try:
            User.objects.get_or_create(
                username=user_data['username'],
                defaults={'password': user_data['password']}
            )
            print(f"Đã tạo user {user_data['username']} thành công!")
        except Exception as e:
            print(f"Lỗi khi tạo user {user_data['username']}: {str(e)}")

    # Tạo thư mục media nếu chưa tồn tại
    media_dir = Path('sql_inject_demo/media/products')
    media_dir.mkdir(parents=True, exist_ok=True)

    # Tạo thư mục static nếu chưa tồn tại
    static_dir = Path('sql_inject_demo/static/images')
    static_dir.mkdir(parents=True, exist_ok=True)

    # Tạo ảnh mặc định nếu chưa tồn tại
    default_image = static_dir / 'no-image.png'
    if not default_image.exists():
        img = Image.new('RGB', (400, 400), color='white')
        img.save(default_image)

    # Tạo danh mục
    categories = {
        'Điện thoại': 'Các loại điện thoại di động',
        'Laptop': 'Máy tính xách tay',
        'Phụ kiện': 'Phụ kiện điện tử'
    }
    
    for name, desc in categories.items():
        Category.objects.get_or_create(
            name=name,
            defaults={'description': desc}
        )

    # Tạo sản phẩm
    products = [
        {
            'name': 'iPhone 13',
            'description': 'iPhone 13 với chip A15 Bionic, camera 12MP',
            'price': 24990000,
            'stock': 50,
            'category': 'Điện thoại',
            'image_url': 'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-13-finish-select-202207-6-1inch-blue?wid=600&hei=600&fmt=jpeg&qlt=95'
        },
        {
            'name': 'Samsung Galaxy S21',
            'description': 'Samsung Galaxy S21 với camera 64MP',
            'price': 19990000,
            'stock': 30,
            'category': 'Điện thoại',
            'image_url': 'https://images.unsplash.com/photo-1610945264803-c22b62d2a7b3?q=80&w=600'
        },
        {
            'name': 'MacBook Pro M1',
            'description': 'MacBook Pro với chip M1, màn hình Retina',
            'price': 32990000,
            'stock': 20,
            'category': 'Laptop',
            'image_url': 'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/mbp14-spacegray-select-202301?wid=600&hei=600&fmt=jpeg&qlt=95'
        },
        {
            'name': 'Dell XPS 13',
            'description': 'Dell XPS 13 với màn hình InfinityEdge',
            'price': 28990000,
            'stock': 15,
            'category': 'Laptop',
            'image_url': 'https://images.unsplash.com/photo-1593642632823-8f785ba67e45?q=80&w=600'
        },
        {
            'name': 'Tai nghe AirPods Pro',
            'description': 'Tai nghe không dây với chống ồn chủ động',
            'price': 5990000,
            'stock': 100,
            'category': 'Phụ kiện',
            'image_url': 'https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?q=80&w=600'
        }
    ]

    for product_data in products:
        try:
            # Tải và xử lý ảnh
            img = download_image(product_data['image_url'])
            if img:
                # Lưu ảnh vào thư mục media
                img_path = media_dir / f"{product_data['name'].lower().replace(' ', '_')}.jpg"
                img.save(img_path, 'JPEG')
            else:
                # Sử dụng ảnh mặc định nếu không tải được
                img_path = default_image
            
            # Tạo sản phẩm với ảnh
            category = Category.objects.get(name=product_data['category'])
            product = Product.objects.create(
                name=product_data['name'],
                description=product_data['description'],
                price=product_data['price'],
                stock=product_data['stock']
            )
            
            # Lưu ảnh cho sản phẩm
            with open(img_path, 'rb') as f:
                product.image.save(
                    f"{product_data['name'].lower().replace(' ', '_')}.jpg",
                    File(f)
                )
            product.save()
            
            # Thêm sản phẩm vào danh mục
            category.products.add(product)
            print(f"Đã tạo sản phẩm {product_data['name']} thành công!")
            
        except Exception as e:
            print(f"Lỗi khi tạo sản phẩm {product_data['name']}: {str(e)}")

    print("Đã thêm dữ liệu mẫu thành công!")

if __name__ == '__main__':
    create_sample_data() 