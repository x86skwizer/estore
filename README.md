# Django E-Commerce Project

This is a Django-based E-Commerce web application. It includes a cart system, payment processing, user authentication, and product/category management. This project demonstrates how to create a fully functioning online store with integration for Stripe payments, user management, and order fulfillment.

---

## Table of Contents
- [Features](#features)
- [Directory Structure](#directory-structure)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Deployment](#deployment)
- [Contributing](#contributing)

---

## Features

1. **User Authentication**  
   - Users can register, log in, and log out.  
   - Profile management (via `Profile` model) is integrated with Django’s `User` model.

2. **Product & Category Management**  
   - Admin users can create, update, and delete products.  
   - Categories allow users to browse products by type.

3. **Shopping Cart**  
   - Add, remove, and update items in the cart.  
   - Cart context is available site-wide via Django context processors.

4. **Stripe Payment Integration**  
   - Users can checkout with Stripe.  
   - Includes success and failure pages, along with custom order handling in the admin dashboard.

5. **Order Management**  
   - Orders and OrderItems are tracked in the admin area.  
   - Track shipping status with separate pages for shipped/not shipped orders.

6. **Responsive Templates**  
   - `base.html` used as a global layout.  
   - A variety of templates for product detail, searching, checkout, and more.

---

## Directory Structure

Below is an overview of the project’s file structure:

```
├── cart
│   ├── cart.py
│   ├── context_processors.py
│   ├── views.py
│   ├── urls.py
│   ├── apps.py
│   ├── admin.py
│   ├── models.py
│   └── templates
│       └── cart_summary.html
├── core
│   ├── views.py
│   ├── urls.py
│   ├── apps.py
│   ├── admin.py
│   ├── models.py
│   ├── forms.py
│   └── templates
│       ├── base.html
│       ├── category.html
│       ├── category_summary.html
│       ├── contact.html
│       ├── index.html
│       ├── login.html
│       ├── my-account.html
│       ├── navbar.html
│       ├── product-detail.html
│       ├── register.html
│       ├── search.html
│       ├── update_info.html
│       └── update_password.html
├── payment
│   ├── views.py
│   ├── urls.py
│   ├── apps.py
│   ├── admin.py
│   ├── models.py
│   ├── forms.py
│   └── templates
│       └── payment
│           ├── billing_info.html
│           ├── checkout.html
│           ├── not_shipped_dash.html
│           ├── orders.html
│           ├── payment_success.html
│           ├── process_failed.html
│           ├── process_order.html
│           ├── shipped_dash.html
│           └── stripe_checkout.html
├── store
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── manage.py
├── requirements.txt
├── runtime.txt
├── procfile
├── static
│   └── store
│       ├── css
│       ├── img
│       ├── js
│       └── lib
├── media
│   └── uploads
│       ├── category
│       └── product
└── db.sqlite3
```

### Notable Files

- **`manage.py`**: Django’s CLI tool for migrations, running the server, etc.  
- **`requirements.txt`**: Lists Python dependencies.  
- **`runtime.txt`**: Specifies the Python runtime version.  
- **`Procfile`**: Used for deploying to platforms like Heroku (Gunicorn server).  

---

## Getting Started

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/django-ecommerce.git
   cd django-ecommerce
   ```

2. **Create and Activate a Virtual Environment** (Recommended)

   ```bash
   python -m venv venv
   source venv/bin/activate   # on Mac/Linux
   venv\Scripts\activate      # on Windows
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**  
   For Stripe payments, you may need environment variables like `STRIPE_SECRET_KEY` and `STRIPE_PUBLISHABLE_KEY`. If required, add them to a `.env` file or configure them in your hosting environment.

5. **Run Migrations**

   ```bash
   python manage.py migrate
   ```

6. **Create a Superuser**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server**

   ```bash
   python manage.py runserver
   ```

8. **Access the Site**  
   Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.  
   - Admin Panel: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## Usage

1. **Local Development**  
   - Make changes in your code.
   - Use `python manage.py runserver` to start the local dev server.
   - Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to see changes.

2. **Adding Products & Categories**  
   - Log in to the Django admin at `/admin/`.
   - Create new `Category` and `Product` entries.

3. **Managing Orders**  
   - The `payment` app handles orders, order items, and shipping.  
   - View or modify orders via the Django admin or the custom dashboards (`shipped_dash`, `not_shipped_dash`).

4. **Shopping Cart**  
   - The cart app provides a site-wide shopping cart (`/cart/urls.py`).

5. **Stripe Payment**  
   - Update your Stripe API keys in the Django settings or environment variables.  
   - The checkout flow is handled by `payment/views.py`.

---

## Deployment

1. **Heroku Example**  
   - Make sure you have the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) installed.
   - Run `heroku create`.
   - Add your environment variables on Heroku (e.g., `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`).
   - Push to Heroku:
     ```bash
     git push heroku main
     ```
   - Heroku will use `Procfile` to run the Gunicorn server and apply migrations automatically if configured properly.

2. **Other Platforms**  
   - Ensure your server can run a Python/Django stack with a WSGI server.  
   - Configure environment variables and static file serving (`whitenoise` or similar).

---

## Contributing

1. Fork this repository.
2. Create your feature branch: `git checkout -b feature/my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature/my-new-feature`
5. Create a new Pull Request.
