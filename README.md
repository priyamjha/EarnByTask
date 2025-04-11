# 📱 EarnByTask

**EarnByTask** is a Django-based web application that allows users to earn points by completing simple Android app-related tasks like downloading and submitting screenshots. Admins can manage apps and confirm task submissions, while users can spend earned points to view fun content like jokes.

---

## 🚀 Features

- 🔐 Custom user authentication with role-based access (User/Admin)
- 📝 Task submission with image upload and admin approval
- 📲 Android app listing with categories and subcategories
- 🧠 Points system to reward user submissions
- 😂 Jokes viewer (deducts points on each view)
- 📊 Dashboards for both users and admins

---

## 📦 Technologies Used

- **Backend**: Django
- **Frontend**: HTML, CSS (with `widget_tweaks` for enhanced form rendering)
- **Database**: SQLite (default, can be changed)
- **Others**: Pillow (for image uploads), Custom Auth Backend, CSV for jokes

---

## 🏗️ App Structure

### Installed Apps

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',  # Core application
    'widget_tweaks',
]
```

---

## 🧩 Key Components

### 🔐 Custom Authentication

- `CustomUser`: Extends Django's `AbstractUser` with fields like `user_type`, `full_name`, `points`, and `email`.
- `CustomUserManager`: Handles user/superuser creation with email validation.
- `MyCustomBackend`: Allows custom login logic using Django's `authenticate()`.

### 📂 Models

- `Category` and `Subcategory`: For classifying Android apps.
- `AndroidApp`: Stores app details like name, logo, download link, category, subcategory, and reward points.
- `TaskSubmission`: Tracks user's proof of task completion, along with admin approval and points awarded.

### 📝 Forms

- `CustomUserCreationForm`: For user registration with validations on username, email, and password.
- `LoginForm`: Extended to support detailed error messages.
- `AndroidAppForm`: Admin form to add/update apps with logo and dropdowns.

### 🧠 Views

- `submit_task`: Allows users to submit proof (image) of app usage.
- `show_joke`: Deducts 20 points to show a joke from a CSV file.
- `view_points` / `view_tasks`: Shows current points and submissions.
- `add_app` / `update_app`: Admin-only features to manage apps.
- `get_subcategories`: AJAX endpoint for dynamically updating subcategories.

---

## 🧪 How to Run Locally

1. **Clone the Repository**

```bash
git clone https://github.com/priyamjha/EarnByTask.git
cd EarnByTask
```

2. **Create Virtual Environment & Install Dependencies**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Run Migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

4. **Create Superuser**

```bash
python manage.py createsuperuser
```

5. **Run the Development Server**

```bash
python manage.py runserver
```

6. **Access the App**

- User Dashboard: `http://localhost:8000/user_dashboard/`
- Admin Dashboard: `http://localhost:8000/admin/`

---

## 📂 File Uploads

- **App logos**: Stored in `media/app_logos/`
- **Task screenshots**: Stored in `media/task_submissions/`

Make sure to add media settings in `settings.py` and serve them during development:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

And update `urls.py`:

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## 🧠 Sample Data (Optional)

Add `onelinefun.csv` in your project root for joke generation. Sample format:

```csv
Joke
Why did the developer go broke? Because he used up all his cache.
```

---

## 🔒 User Types

- **Admin**: Can add/update apps and confirm task submissions.
- **User**: Can register, submit tasks, view points, and see jokes.

---

## 📃 License

This project is licensed under the MIT License.

---
