
📄 MUSIC BEATS PROJECT - BACKEND ROADMAP (PHASE 1 COMPLETE ✅)
Author: Gopi | Date: May 18, 2025
Goal: Build a smart web app for managing a music institute (users, fees, attendance, schedules)

---

👣 STAGE 1: PROJECT SETUP AND CUSTOM USER SYSTEM

1️⃣ SETTING UP THE ENVIRONMENT

- First, I created a **virtual environment** using:
    python -m venv venv
- Then activated it using:
    .\venv\Scripts\Activate.ps1   (on Windows)

🧠 Why?  
A virtual environment keeps all project dependencies separate from global Python, so nothing breaks.

---

2️⃣ CREATING THE DJANGO PROJECT

- Ran this to create the project:
    django-admin startproject backend .

🧠 This made a new `backend/` folder with Django's core settings, ready to build apps inside.

---

3️⃣ CREATING OUR FIRST APP: ACCOUNTS

- Inside the project, I ran:
    python manage.py startapp accounts

🧠 This app will handle user registration, login, logout, and profile logic.

---

4️⃣ REGISTERING THE ACCOUNTS APP

- In `backend/settings.py`, I added:
    'accounts',

🧠 This tells Django to include the app in the project.

---

5️⃣ BUILDING A CUSTOM USER MODEL

- Inside `accounts/models.py`, I created a new class:
```python
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
````

🧠 Why Custom User?
We want login with **email** instead of username, and flexibility for future roles like student/teacher/admin.

---

6️⃣ TELLING DJANGO TO USE OUR CUSTOM USER

* In `backend/settings.py`, added:
  AUTH\_USER\_MODEL = 'accounts.CustomUser'

🧠 Now Django knows to ignore its default user model and use ours instead.

---

7️⃣ MAKING MIGRATIONS

* First created migration scripts:
  python manage.py makemigrations accounts

* Then applied them to DB:
  python manage.py migrate

🧠 This created tables in the SQLite database for our CustomUser model and other Django defaults.

---

8️⃣ CREATED SUPERUSER (ADMIN)

* Ran:
  python manage.py createsuperuser

* Gave it email, full name, and password.

🧠 This allows logging into Django’s admin panel.

---

👣 STAGE 2: ADDING JWT AUTHENTICATION SYSTEM

---

9️⃣ REPLACED `authtoken` WITH JWT (JSON Web Token)

Initially, I had used Django’s old token auth which gives **1 static token per user.** That’s not ideal.

So I removed `rest_framework.authtoken` and installed JWT package:

```bash
pip install djangorestframework-simplejwt
```

🧠 Why JWT?

* Safer: tokens expire.
* Refreshable: you don’t stay logged in forever.
* Supports blacklist (for logout).
* Good for mobile/web frontend.

---

🔟 CONFIGURED SIMPLEJWT IN SETTINGS

Added this in `settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    ...
}
```

Also added:

```python
'rest_framework_simplejwt.token_blacklist',
```

to `INSTALLED_APPS`

🧠 Now, our system is ready to generate and handle JWT tokens.

---

1️⃣1️⃣ SETUP JWT AUTH URL ROUTES

In `accounts/urls.py`, added:

```python
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
```

Now available endpoints:

* POST `/api/v1/accounts/token/` – Get access + refresh tokens (login)
* POST `/api/v1/accounts/token/refresh/` – Get new access token
* POST `/api/v1/accounts/logout/` – Send refresh token to logout

---

1️⃣2️⃣ BUILT A CUSTOM LOGIN RESPONSE

By default, JWT login only returns tokens.

So I **overrode the serializer** (`CustomTokenObtainPairSerializer`) to include:

* email
* full\_name
* is\_staff
* is\_superuser

🧠 This makes frontend login easier — it gets user info directly with tokens.

---

1️⃣3️⃣ BUILT A USER PROFILE SERIALIZER

```python
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'full_name']
```

🧠 Now you can reuse this to show user info anywhere (like dashboard/profile page).

---

1️⃣4️⃣ HANDLED LOGOUT USING BLACKLIST

JWT tokens don’t “expire” on logout by default. So we created a view to:

* Accept the refresh token
* Blacklist it using `OutstandingToken` model

🧠 This means: after logout, that refresh token is no longer usable.

---

📉 ERROR I FACED: MIGRATION CONFLICT

When I added new fields (`first_name`, `last_name`) to the CustomUser model **after migrating**, Django asked for default values.

I tried using `default=""` but then it created a weird migration.

✅ Solution: I ran:

```bash
python manage.py flush  # reset entire DB
python manage.py makemigrations
python manage.py migrate
```

🧠 Lesson: Add all necessary fields early or handle default values properly.

---

✅ FINAL STAGE: MANUAL TESTING OF AUTH SYSTEM

I tested every endpoint manually using Postman:

| Endpoint          | Purpose                        | Status  |
| ----------------- | ------------------------------ | ------- |
| `/register/`      | Created test user              | ✅ Works |
| `/token/`         | Logged in, got tokens          | ✅ Works |
| `/token/refresh/` | Got new access token           | ✅ Works |
| `/logout/`        | Sent refresh token, logged out | ✅ Works |

I also tested:

* Reusing blacklisted tokens ❌ (correctly fails)
* Missing token headers ❌ (correctly fails)
* Wrong content types (e.g., plain text) ❌
* Invalid paths (404) ❌

🧠 All security checks are working as expected.

---

🧠 WHAT I LEARNED DEEPLY

* How Django apps and projects are structured
* Why virtual environments matter
* What “migrations” do and how to reset them safely
* How to override Django’s user model properly
* What JWT is, how it works, and how it’s better than static tokens
* How to handle login, logout, token rotation securely
* How to test APIs properly and read backend error messages

---

🚀 WHAT'S NEXT?

1. Define user roles (admin, teacher, student)
2. Protect certain views using role-based permissions
3. Build a `/profile/` API to fetch/update logged-in user data
4. Start connecting with frontend using HTML + JS
5. Add next modules: attendance, scheduling, fees

---

🧭 This is how I built the complete user auth system for MUSIC BEATS.
