"""
A list of strings representing the host/domain names that this Django site can serve.
This is a security measure to prevent HTTP Host header attacks, which are possible even
under many seemingly-safe web server configurations.

* https://docs.djangoproject.com/en/4.1/ref/settings/#allowed-hosts
"""
ALLOWED_HOSTS: list[str] = []
