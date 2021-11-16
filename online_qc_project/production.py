"""
Django production settings for esite project.

For more information on this file, see
https://docs.djangoproject.com/en/stable/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/stable/ref/settings/

This development settings are unsuitable for production, see
https://docs.djangoproject.com/en/stable/howto/deployment/checklist/
"""

import random
import string

import dj_database_url
import django_cache_url

from .base import *  # noqa

# > Debug Switch
# SECURITY WARNING: don't run with debug turned on in production!
# IMPORTANT: Specified in the environment or set to default (off).
# See https://docs.djangoproject.com/en/stable/ref/settings/#debug
DEBUG = env.get("DJANGO_DEBUG", "off") == "on"

# > DEBUG_PROPAGATE_EXCEPTIONS Switch
# SECURITY WARNING: don't run with debug turned on in production!
# IMPORTANT: Specified in the environment or set to default (off).
# See https://docs.djangoproject.com/en/stable/ref/settings/#debug
DEBUG_PROPAGATE_EXCEPTIONS = env.get("DJANGO_DEBUG_PROPAGATE_EXCEPTIONS", "off") == "on"

# This is used by Wagtail's email notifications for constructing absolute
# URLs. Please set to the domain that users will access the admin site.
if "PRIMARY_HOST" in env:
    BASE_URL = "https://{}".format(env["PRIMARY_HOST"])

# > Secret Key
# SECURITY WARNING: keep the secret key used in production secret!
# IMPORTANT: Specified in the environment or generate an ephemeral key.
# See https://docs.djangoproject.com/en/stable/ref/settings/#secret-key
if "DJANGO_SECRET_KEY" in env:
    SECRET_KEY = env["DJANGO_SECRET_KEY"]
else:
    # Use if/else rather than a default value to avoid calculating this,
    # if we don't need it.
    print(
        "WARNING: DJANGO_SECRET_KEY not found in os.environ. Generating ephemeral SECRET_KEY."
    )
    SECRET_KEY = "".join(
        [random.SystemRandom().choice(string.printable) for i in range(50)]
    )

# https://docs.djangoproject.com/en/dev/ref/settings/#prepend-www
if "PREPEND_WWW" in env:
    PREPEND_WWW = env["PREPEND_WWW"]

if "GOOGLE_TAG_MANAGER_ID" in env:
    GOOGLE_TAG_MANAGER_ID = env["GOOGLE_TAG_MANAGER_ID"]

# > SSL Header
# Used to detect secure connection proberly on Heroku.
# See https://wagtail.io/blog/deploying-wagtail-heroku/
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# > SSL Redirect
# Every rquest gets redirected to HTTPS
SECURE_SSL_REDIRECT = env.get("DJANGO_SECURE_SSL_REDIRECT", "off") == "on"

# > Allowed Hosts
# Accept all hostnames, since we don't know in advance
# which hostname will be used for any given Docker instance.
# IMPORTANT: Set this to a real hostname when using this in production!
# See https://docs.djangoproject.com/en/stable/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.get("DJANGO_ALLOWED_HOSTS", "*").split(";")

# Set s-max-age header that is used by reverse proxy/front end cache. See
# urls.py.
try:
    CACHE_CONTROL_S_MAXAGE = int(env.get("CACHE_CONTROL_S_MAXAGE", 600))
except ValueError:
    pass

# Give front-end cache 30 second to revalidate the cache to avoid hitting the
# backend. See urls.py.
CACHE_CONTROL_STALE_WHILE_REVALIDATE = int(
    env.get("CACHE_CONTROL_STALE_WHILE_REVALIDATE", 30)
)

# > Security Configuration
# This configuration is required to achieve good security rating.
# You can test it using https://securityheaders.com/
# https://docs.djangoproject.com/en/stable/ref/middleware/#module-django.middleware.security

# > Force HTTPS Redirect
# https://docs.djangoproject.com/en/stable/ref/settings/#secure-ssl-redirect
if env.get("SECURE_SSL_REDIRECT", "true").strip().lower() == "true":
    SECURE_SSL_REDIRECT = False

# This will allow the cache to swallow the fact that the website is behind TLS
# and inform the Django using "X-Forwarded-Proto" HTTP header.
# https://docs.djangoproject.com/en/stable/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# This is a setting setting HSTS header. This will enforce the visitors to use
# HTTPS for an amount of time specified in the header. Please make sure you
# consult with sysadmin before setting this.
# https://docs.djangoproject.com/en/stable/ref/settings/#secure-hsts-seconds
if "SECURE_HSTS_SECONDS" in env:
    SECURE_HSTS_SECONDS = int(env["SECURE_HSTS_SECONDS"])

# https://docs.djangoproject.com/en/stable/ref/settings/#secure-browser-xss-filter
if env.get("SECURE_BROWSER_XSS_FILTER", "true").lower().strip() == "true":
    SECURE_BROWSER_XSS_FILTER = True

# https://docs.djangoproject.com/en/stable/ref/settings/#secure-content-type-nosniff
if env.get("SECURE_CONTENT_TYPE_NOSNIFF", "true").lower().strip() == "true":
    SECURE_CONTENT_TYPE_NOSNIFF = True

# > Email Settings
# We use SMTP to send emails. We typically use transactional email services
# that let us use SMTP.
# https://docs.djangoproject.com/en/2.1/topics/email/

# https://docs.djangoproject.com/en/stable/ref/settings/#email-host
if "DJANGO_EMAIL_HOST" in env:
    EMAIL_HOST = env["DJANGO_EMAIL_HOST"]

# https://docs.djangoproject.com/en/stable/ref/settings/#email-port
if "DJANGO_EMAIL_PORT" in env:
    try:
        EMAIL_PORT = int(env["DJANGO_EMAIL_PORT"])
    except ValueError:
        pass

# https://docs.djangoproject.com/en/stable/ref/settings/#email-host-user
if "DJANGO_EMAIL_HOST_USER" in env:
    EMAIL_HOST_USER = env["DJANGO_EMAIL_HOST_USER"]

# https://docs.djangoproject.com/en/stable/ref/settings/#email-host-password
if "DJANGO_EMAIL_HOST_PASSWORD" in env:
    EMAIL_HOST_PASSWORD = env["DJANGO_EMAIL_HOST_PASSWORD"]

# https://docs.djangoproject.com/en/stable/ref/settings/#email-use-tls
if env.get("DJANGO_EMAIL_USE_TLS", "false").lower().strip() == "true":
    EMAIL_USE_TLS = True

# https://docs.djangoproject.com/en/stable/ref/settings/#email-use-ssl
if env.get("DJANGO_EMAIL_USE_SSL", "false").lower().strip() == "true":
    EMAIL_USE_SSL = True

# https://docs.djangoproject.com/en/stable/ref/settings/#email-subject-prefix
if "DJANGO_EMAIL_SUBJECT_PREFIX" in env:
    EMAIL_SUBJECT_PREFIX = env["DJANGO_EMAIL_SUBJECT_PREFIX"]

# SERVER_EMAIL is used to send emails to administrators.
# https://docs.djangoproject.com/en/stable/ref/settings/#server-email
# DEFAULT_FROM_EMAIL is used as a default for any mail send from the website to
# the users.
# https://docs.djangoproject.com/en/stable/ref/settings/#default-from-email
if "DJANGO_SERVER_EMAIL" in env:
    SERVER_EMAIL = DEFAULT_FROM_EMAIL = env["DJANGO_SERVER_EMAIL"]

# > Database Configuration
# See https://pypi.org/project/dj-database-url/
# See https://docs.djangoproject.com/en/stable/ref/settings/#databases
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES["default"].update(db_from_env)

# Configure caches from cache url
CACHES = {"default": django_cache_url.config()}

# > Front-end Cache
# This configuration is used to allow purging pages from cache when they are
# published.
# These settings are usually used only on the production sites.
# This is a configuration of the CDN/front-end cache that is used to cache the
# production websites.
# https://docs.wagtail.io/en/latest/reference/contrib/frontendcache.html
# You are required to set the following environment variables:
#  * FRONTEND_CACHE_CLOUDFLARE_TOKEN
#  * FRONTEND_CACHE_CLOUDFLARE_EMAIL
#  * FRONTEND_CACHE_CLOUDFLARE_ZONEID
# Can be obtained from a sysadmin.
if "FRONTEND_CACHE_CLOUDFLARE_TOKEN" in env:
    INSTALLED_APPS.append("wagtail.contrib.frontend_cache")
    WAGTAILFRONTENDCACHE = {
        "default": {
            "BACKEND": "wagtail.contrib.frontend_cache.backends.CloudflareBackend",
            "EMAIL": env["FRONTEND_CACHE_CLOUDFLARE_EMAIL"],
            "TOKEN": env["FRONTEND_CACHE_CLOUDFLARE_TOKEN"],
            "ZONEID": env["FRONTEND_CACHE_CLOUDFLARE_ZONEID"],
        }
    }

# > Logging
# This logging is configured to be used with Sentry and console logs. Console
# logs are widely used by platforms offering Docker deployments, e.g. Heroku.
# We use Sentry to only send error logs so we're notified about errors that are
# not Python exceptions.
# We do not use default mail or file handlers because they are of no use for
# us.
# https://docs.djangoproject.com/en/stable/topics/logging/
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        # Send logs with at least INFO level to the console.
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        # Send logs with level of at least ERROR to Sentry.
        #'sentry': {
        #    'level': 'ERROR',
        #    'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        # },
    },
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s][%(process)d][%(levelname)s][%(name)s] %(message)s"
        }
    },
    "loggers": {
        "esite": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "wagtail": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "django.request": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "django.security": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}

# Add embeds for streamfield.
if "EMBEDLY_API_KEY" in env:
    WAGTAILEMBEDS_FINDERS = [
        {"class": "wagtail.embeds.finders.embedly", "key": env["EMBEDLY_API_KEY"]}
    ]

# MIDDLEWARE.append('django_referrer_policy.middleware.ReferrerPolicyMiddleware')

# Referrer-policy header settings.
# https://django-referrer-policy.readthedocs.io/en/1.0/
# REFERRER_POLICY = env.get('SECURE_REFERRER_POLICY', 'no-referrer-when-downgrade').strip()

# Content Security policy settings
# http://django-csp.readthedocs.io/en/latest/configuration.html
# if 'CSP_DEFAULT_SRC' in env:
#    MIDDLEWARE.append('csp.middleware.CSPMiddleware')

# The “special” source values of 'self', 'unsafe-inline', 'unsafe-eval', and 'none' must be quoted!
# e.g.: CSP_DEFAULT_SRC = "'self'" Without quotes they will not work as intended.

#    CSP_DEFAULT_SRC = env.get('CSP_DEFAULT_SRC').split(',')
#    if 'CSP_SCRIPT_SRC' in env:
#        CSP_SCRIPT_SRC = env.get('CSP_SCRIPT_SRC').split(',')
#    if 'CSP_STYLE_SRC' in env:
#        CSP_STYLE_SRC = env.get('CSP_STYLE_SRC').split(',')
#    if 'CSP_IMG_SRC' in env:
#        CSP_IMG_SRC = env.get('CSP_IMG_SRC').split(',')
#    if 'CSP_CONNECT_SRC' in env:
#        CSP_CONNECT_SRC = env.get('CSP_CONNECT_SRC').split(',')
#    if 'CSP_FONT_SRC' in env:
#        CSP_FONT_SRC = env.get('CSP_FONT_SRC').split(',')
#    if 'CSP_BASE_URI' in env:
#        CSP_BASE_URI = env.get('CSP_BASE_URI').split(',')
#    if 'CSP_OBJECT_SRC' in env:
#        CSP_OBJECT_SRC = env.get('CSP_OBJECT_SRC').split(',')

# > Recaptcha
# These settings are required for the captcha challange to work.
# https://github.com/springload/wagtail-django-recaptcha
if "RECAPTCHA_PUBLIC_KEY" in env and "RECAPTCHA_PRIVATE_KEY" in env:
    NOCAPTCHA = True
    RECAPTCHA_PUBLIC_KEY = env["RECAPTCHA_PUBLIC_KEY"]
    RECAPTCHA_PRIVATE_KEY = env["RECAPTCHA_PRIVATE_KEY"]

# > Telegram backend
# The backend to use for sending telegrams.
TELEGRAM_API_ID = os.getenv("TELEGRAM_API_ID", "")
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2019-2020 Simon Prast
