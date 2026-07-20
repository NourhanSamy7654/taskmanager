# 🗂️ Task Manager

A Django-based task management system with authentication and REST API support.

---
### Swagger API Documentation

![Dashboard And All Tasks ](/taskManager/screen/s2.png)

### Tasks

![Swagger](/taskManager/screen/s1.png)

## ✨ Key Features

* User authentication (register / login)
* Full CRUD operations for tasks
* Task status & priority tracking
* User-specific data isolation
* REST API with token authentication
* Swagger / OpenAPI documentation

---

## 🛠️ Tech Stack

* Django 5.2
* Django REST Framework
* PostgreSQL
* drf-spectacular

---

## 🚀 Getting Started

### 1. Clone project

```bash
git clone <repo-url>
cd task-manager
```

### 2. Create virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create `.env` file:

```env
SECRET_KEY=your_secret_key
DEBUG=True

DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Run server

```bash
python manage.py runserver
```

---

## 🌐 API Endpoints

* `GET/POST /api/v1/tasks/` — list & create tasks
* `GET/PUT/DELETE /api/v1/tasks/<id>/` — task details
* `POST /api/v1/auth/register/` — register user
* `POST /api/v1/auth/token/` — obtain token
* `/swagger/` — API documentation
* `/api/schema/` — OpenAPI schema

---

