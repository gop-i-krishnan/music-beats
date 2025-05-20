
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

👣 **STAGE 3: PAYMENT MODULE - FEE MANAGEMENT**

---

1️⃣ CREATED `payments` APP

* Ran inside backend:

  ```bash
  python manage.py startapp payments
  ```
* This app will manage all fee records, summaries, and payments.

---

2️⃣ DEFINED FEE RECORD MODEL

* In `payments/models.py`, created `FeeRecord` model to track individual fee payments, including:

```python
class FeeRecord(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateField(auto_now_add=True)
    remarks = models.TextField(blank=True, null=True)
```

---

3️⃣ CREATED SERIALIZERS FOR FEE RECORDS

* In `payments/serializers.py`, created `FeeRecordSerializer` for easy conversion between model and JSON.

---

4️⃣ ADDED VIEWS TO HANDLE FEE RECORDS

* Used Django REST Framework generic views:

  * `FeeRecordListCreateView`: List all fees or create a new fee payment.
  * `FeeRecordRetrieveUpdateDestroyView`: Get, update or delete a fee record by ID.
* Created custom APIViews for:

  * `FeeSummaryView`: Summary of fees paid by a student in a date range.
  * `overall_fee_summary`: Overall total payments and count for the institute.

---

5️⃣ DEFINED URL ROUTES FOR PAYMENTS APP

* In `payments/urls.py`, routes include:

```python
from django.urls import path
from .views import FeeRecordListCreateView, FeeSummaryView, FeeRecordRetrieveUpdateDestroyView, overall_fee_summary

urlpatterns = [
    path('fees/', FeeRecordListCreateView.as_view(), name='fee-list-create'),
    path('fees/<int:pk>/', FeeRecordRetrieveUpdateDestroyView.as_view(), name='fee-detail'),
    path('fees/<int:student_id>/summary/', FeeSummaryView.as_view(), name='fee-summary'),
    path('fees/summary/overall/', overall_fee_summary, name='fee-overall-summary'),
]
```

---

6️⃣ INCLUDED PAYMENTS APP URLS IN PROJECT `core/urls.py`

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/accounts/', include('accounts.urls')),
    path('api/v1/attendance/', include('attendance.urls')),
    path('api/v1/payments/', include('payments.urls')),
    path('api/v1/accounts/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/accounts/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

---

7️⃣ TESTED PAYMENT ENDPOINTS USING POSTMAN

| Endpoint                                      | Purpose                             | Status  |
| --------------------------------------------- | ----------------------------------- | ------- |
| `/api/v1/payments/fees/`                      | List and create fee records         | ✅ Works |
| `/api/v1/payments/fees/<int:pk>/`             | Retrieve, update, delete fee record | ✅ Works |
| `/api/v1/payments/fees/<student_id>/summary/` | Student fee summary with filters    | ✅ Works |
| `/api/v1/payments/fees/summary/overall/`      | Overall institute fee summary       | ✅ Works |

---

🧠 **WHAT I LEARNED DEEPLY IN PAYMENTS MODULE**

* How to create modular apps and isolate functionality
* Using Django REST Framework generics for CRUD APIs
* Building custom summary APIs with filtering parameters
* Including app URLs inside project URL configuration
* Testing and debugging 404 errors caused by URL mismatches
* Using Django query filters and aggregation functions for reports

---

🚀 **WHAT'S NEXT?**

1. Implement role-based permissions (admin/teacher/student)
2. Build attendance management module APIs
3. Create user profile and settings APIs
4. Start working on the frontend UI integration with these APIs
5. Add scheduling and notifications module

---

🧭 This is how I built the user authentication and payments systems for MUSIC BEATS backend so far.

---

If you want, I can help you generate a nicely formatted markdown or README file ready to commit. Would you like that?
