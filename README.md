# MiniShop - E-commerce Website


### Cài đặt
1. Clone repo 

2.	Cài đặt requirements:
```bash
 pip install -r requirements.txt
```

3. Chạy migrations:
```bash
python manage.py migrate
```

4. Load dữ liệu mẫu:
```bash
python manage.py loaddata fixtures/data.json
```

5. Chạy development server:
```bash
pip install whitenoise
python manage.py collectstatic

daphne -p 8000 minishop.asgi:application

```

6. Truy cập: http://127.0.0.1:8000/

## Tài khoản mẫu

### Admin
- Username: `admin`
- Password: `admin123`
- URL: http://127.0.0.1:8000/admin/

## Cấu trúc project

```
minishop/
├── minishop/           # Main project settings
├── products/           # Product management app
├── accounts/           # User authentication app
├── cart/              # Shopping cart app
├── orders/            # Order management app
├── templates/         # HTML templates
├── static/           # CSS, JS, images
├── media/            # User uploaded files
└── manage.py         # Django management script
```


### Các model chính:
- **Category**: Danh mục sản phẩm
- **Product**: Sản phẩm với thông tin chi tiết
- **Profile**: Hồ sơ người dùng mở rộng
- **Order**: Đơn hàng
- **OrderItem**: Chi tiết sản phẩm trong đơn hàng
- **Review**: Đánh giá sản phẩm
