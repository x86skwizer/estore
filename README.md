# Django E-Commerce Project

A **fully-featured** Django E-Commerce application with shopping cart functionality, secure payment integration (Stripe), user authentication, and product/category management. This repository demonstrates a complete online store, including product searches, order tracking, shipping dashboard, and a responsive front-end.

---

## Table of Contents

1. [Features](#features)
2. [Directory Structure](#directory-structure)
3. [Getting Started](#getting-started)
4. [Usage](#usage)
5. [Deployment](#deployment)
6. [Contributing](#contributing)

---

## Features

1. **User Authentication**  
   - Register, log in/out, update profile info.  
   - Extended `Profile` model linked with Django’s `User`.

2. **Product & Category Management**  
   - Create, update, and delete products/categories via Django admin.  
   - Clear category-based navigation in the user interface.

3. **Shopping Cart**  
   - Cart context processor for site-wide cart access.  
   - Add, remove, and update item quantities on the fly.

4. **Stripe Payment Integration**  
   - Seamless checkout with Stripe.  
   - Payment success/failure pages, plus a fully trackable ordering system.

5. **Order Management & Shipping**  
   - Admin dashboard for shipped/unshipped orders.  
   - Automatically updates shipping status and records order details.

6. **Responsive UI**  
   - `base.html` layout with partials (e.g., `navbar.html`).  
   - Integrates slick sliders, category highlights, and an overall modern design.

---

## Directory Structure

Below is a high-level overview of the project’s structure:

```
├── cart
│   ├── cart.py
│   ├── context_processors.py
│   ├── urls.py
│   ├── views.py
│   ├── models.py
│   └── templates
│       └── cart_summary.html
├── core
│   ├── forms.py
│   ├── urls.py
│   ├── views.py
│   ├── models.py
│   └── templates
│       ├── base.html
│       ├── category.html
│       ├── product-detail.html
│       └── ...
├── payment
│   ├── urls.py
│   ├── views.py
│   ├── models.py
│   └── templates
│       └── payment
│           ├── checkout.html
│           ├── payment_success.html
│           └── ...
├── store
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── static
│   └── store
│       ├── css
│       ├── js
│       └── lib
├── media
│   └── uploads
│       ├── category
│       └── product
├── manage.py
├── requirements.txt
├── runtime.txt
└── procfile
```

### Notable Files

- **`manage.py`**: Django’s CLI tool for database migrations, running the dev server, etc.
- **`requirements.txt`**: Contains project dependencies.
- **`runtime.txt`**: Specifies Python version (useful for deployment on Heroku).
- **`Procfile`**: Used by Heroku to run the Gunicorn server for this Django app.

---

## Getting Started

1. **Clone the Repository**

   ```bash
   git clone https://github.com/x86skwizer/django-ecommerce.git
   cd django-ecommerce
   ```

2. **Create and Activate a Virtual Environment** (Recommended)

   ```bash
   python -m venv venv
   source venv/bin/activate        # Mac/Linux
   venv\Scripts\activate           # Windows
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables (Stripe, etc.)**  
   - If you’re using Stripe locally, set `STRIPE_SECRET_KEY` and `STRIPE_PUBLIC_KEY` in a `.env` file or in your shell.  
   - For email sending, ensure you have the correct SMTP settings.

5. **Apply Migrations**

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

8. **Access the Application**  
   - Frontend: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)  
   - Admin Panel: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## Usage

- **Local Development**: Make your changes, then run `python manage.py runserver`.  
- **Managing Products**: Create/edit products and categories via the admin panel.  
- **Shopping Cart**: Browse and add items to your cart.  
- **Order/Shipping**: If you’re logged in as an admin or superuser, track shipped/unshipped orders in the payment dashboards.  
- **Stripe Checkout**: Test payments locally or in staging by configuring Stripe keys.

---

## Deployment

1. **Heroku Example**  
   - Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).  
   - Run `heroku create` to create a new app.  
   - Set environment variables (Stripe keys, etc.) on Heroku.  
   - Push the repository:

     ```bash
     git push heroku main
     ```

   - Heroku will read the `Procfile` and use Gunicorn to serve the application.

2. **Other Platforms**  
   - Configure your environment variables and static files.  
   - Use a WSGI server like Gunicorn or uWSGI.

---

## Contributing

1. **Fork** this repository.  
2. **Create a Feature Branch** (`git checkout -b feature/my-new-feature`).  
3. **Commit Changes** (`git commit -am 'Add some feature'`).  
4. **Push** to the branch (`git push origin feature/my-new-feature`).  
5. **Open a Pull Request** on this repo.
