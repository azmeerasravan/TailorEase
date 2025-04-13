# 👗 TailorEase –Custom Tailoring Platform

TailorEase is a Django-based web application that enables seamless online custom tailoring experiences for customers and vendors. The platform supports role-based access, product management, fabric recommendations, cart functionality, and order.

## 🚀 Features

- 👤 User Authentication & Role Upgrades (Customer ↔ Vendor)
- 🧵 Vendors can:
  - Add garments with model, size, price, image
  - Manage inventory and orders via dashboard
- 🛍️ Customers can:
  - Browse products
  - Add to Cart, Customize or Purchase
  - Submit measurement details
  - Track orders
- 📦 Order management for both roles
- 🧾 Profile view with role-specific fields

## 🛠️ Tech Stack

- Backend: Django, Django REST Framework
- Frontend: Django Templates + Bootstrap
- Database: SQLite3

---

## 🧑‍💻 Installation Guide

### Prerequisites

- Python 3.8+
- PostgreSQL
- Git
- pip / virtualenv

### Clone the repository

```bash
git clone https://github.com/azmeerasravan/TailorEase.git
cd TailorEase

python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt

### Apply migrations
python manage.py makemigrations
python manage.py migrate

python manage.py runserver
```

Login Page
![Login Page](Docs/UI_images/Login_Page.png)


Sign in Page
![Sign In Page](Docs/UI_images/Signin_Page.png)

Customer Interface
![Customer Interface](Docs/UI_images/Customer_interface.png)

Customer Dashboard
![Customer Dashboard](Docs/UI_images/Customer_Dashboard.png)

View Product
![View Product](Docs/UI_images/Customer_View_Product.png)

Customize Product
![Customize Product](Docs/UI_images/Customer_Customize_Product.png)

Customer Cart
![Customer Cart](Docs/UI_images/Cart_Page.png)

Cutomer Order Tracking
![Cutomer Order Tracking](Docs/UI_images/Orders_Page.png)

Customer Profile
![Customer Profile](Docs/UI_images/Customer_Profile.png)

Payment Interface
![Payment Interface](Docs/UI_images/Payment_Page.png)

Vendor Interface
![Vendor Interface](Docs/UI_images/Vendors_Interface.png)

Vendor Dashboard
![Vendor Dashboard](Docs/UI_images/Vendor_Dashboard.png)

Orders Received
![Orders Received](Docs/UI_images/Vendors_Order_Page.png)

Add Product
![Add Product](Docs/UI_images/Vednor_Add_Product.png)

Add Fabric
![Add Fabric](Docs/UI_images/Vendor_Add_Fabric.png)

Edit Product
![Edit Product](Docs/UI_images/Vendor_Edit_Product.png)

Vendor Profile
![Vendor Profile](Docs/UI_images/Vendor_Profile.png)


