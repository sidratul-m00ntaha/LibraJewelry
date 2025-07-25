# 💎 Libra Jewelry – Django E-commerce Web App

Welcome to **Libra Jewelry**, an online jewelry shop web application built using Django and Bootstrap.  
This project transforms a traditional offline jewelry store into a scalable, secure, and elegant digital storefront.

---

## 🔧 Tech Stack

- **Backend**: Django, SQLite
- **Frontend**: HTML, CSS (Bootstrap 5), Django Template Language
- **Authentication**: Django Auth with email verification

---

## 🌟 Key Features

- ✅ User Registration & Login (with Email Verification)
- 🛍️ Product Browsing by Categories
- 🛒 Add to Cart and Checkout
- 🧾 Order History and Invoice
- 🛡️ CSRF Protection, Form Validation, Auth Middleware
- 📦 Admin Panel for Managing Products, Orders & Users

---

## 🚀 Getting Started

Follow these steps to run the project locally:

### 1️⃣ Clone the Repo

```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
```
### 2️⃣ Set Up a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate        # On Linux/Mac
venv\Scripts\activate           # On Windows
```
### 3️⃣ Install Requirements
```bash
pip install -r requirements.txt
```
### 4️⃣ Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```
### 5️⃣ Create Superuser (Optional)
```bash
python manage.py createsuperuser
```
### 6️⃣ Run the Development Server
```bash
python manage.py runserver
```


