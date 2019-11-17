INSTALLED_APPS = (
    'e_contact',
    'tests',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'e_contact_tests.db'
    },
}

SECRET_KEY = 'unused'

print('In test_settings...')
