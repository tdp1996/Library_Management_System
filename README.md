# Library Management System

Library Management System is a web application designed to streamline library operations, manage books, users, and borrowing transactions efficiently. Built with Django and MySQL, it provides an intuitive interface for both users and administrators to handle library data seamlessly.

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [System Requirements](#system-requirements)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Project Structure](#project-structure)
7. [Notes](#notes)
8. [Contact](#contact)

## Introduction

The Library Management System offers a user-friendly platform to handle library activities such as:
- User registration, login, and profile management.
- Managing books by genre and author.
- Viewing and borrowing books.
- Managing book transactions like borrow and return.

This project was built using Django as a practice exercise and utilizes MySQL as the database backend.

## Features

### User
- Register, login, and update personal information.
- View a list of available books and borrow books.
- Manage personal borrow records.

### Admin
- Manage users: add, edit, delete user information.
- Manage books: add, edit, delete book records.
- Manage borrow/return transactions and fees.

### Additional Features
- Search books by title, author, or genre.
- Track borrowing status and fines (if applicable).

## System Requirements

- Python 3.10+
- Django 5.1+
- MySQL 8.0+
- Additional Python libraries (listed in `requirements.txt`)

## Installation

### Step 1: Clone the repository
```bash
git clone https://github.com/username/Library-Management-System.git
cd Library-Management-System
```

### Step 2: Create a virtual environment and install required packages
```bash
conda env create -f env.yml
```

### Step 3: Configure MySQL database
Create a MySQL database and update the settings.py file with your database information:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_database_name',
        'USER': 'root',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### Step 4: Migrate and create a superuser
```bash
# Apply database migrations
python manage.py makemigrations
python manage.py migrate

# Create a superuser account
python manage.py createsuperuser
```

### Step 5: Run the server
```bash
python manage.py runserver
```
Now, you can access the application at http://127.0.0.1:8000.

## Usage
1. Go to the login page at http://127.0.0.1:8000/login/ and log in with your admin account.
2. Navigate to the Admin page (http://127.0.0.1:8000/admin/) to manage books and users.
3. Search books by title, author, or genre.
4. Borrow books and track your borrowing status.

## Project Structure
```
Library-Management-System/
├── library_management
    ├── library/                 # Main Django application
    │   ├── migrations/          # Database migration files
    │   ├── static/              # CSS, JS, and image files
    │   ├── templates/           # HTML templates for front-end
    │   ├── models.py            # Data models for the application
    │   ├── views.py             # View logic for displaying pages
    │   ├── admin.py             # Admin site configurations
    │   └── urls.py              # URL routing for the application
    │
    ├── manage.py                # Django management script
    ├── requirements.txt         # Required Python libraries
    └── README.md                # This README file
```

## Notes
- Ensure the database configuration is correct before running migrations.
- If you encounter issues with cache or UI updates, try clearing your browser cache or deleting old static files.
