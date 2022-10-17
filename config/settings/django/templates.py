"""
Being a web framework, Django needs a convenient way to generate HTML dynamically. The
most common approach relies on templates. A template contains the static parts of the
desired HTML output as well as some special syntax describing how dynamic content will
be inserted.

* https://docs.djangoproject.com/en/4.1/topics/templates/
"""
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
