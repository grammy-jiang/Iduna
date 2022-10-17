"""
Middleware is a framework of hooks into Django’s request/response processing. It’s a
light, low-level “plugin” system for globally altering Django’s input or output.

* https://docs.djangoproject.com/en/4.1/topics/http/middleware/
"""
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
