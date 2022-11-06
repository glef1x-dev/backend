# Application definition

APPS = [
    'app',
    'a12n',
    'users',
    'blog'
]

HEALTH_CHECKS_APPS = [
    'health_check',
    'health_check.db',
]

THIRD_PARTY_APPS = [
    'corsheaders',
    'drf_spectacular',
    'drf_spectacular_sidecar',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'axes',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',

    'baton',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'baton.autodiscover'
]

INSTALLED_APPS = APPS + HEALTH_CHECKS_APPS + THIRD_PARTY_APPS
