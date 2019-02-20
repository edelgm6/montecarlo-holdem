# montecarlo-poker
montecarlo-poker is a Texas Hold Em Montecarlo simulator to calculate the probability of different hands and win frequency. It is hosted at [https://montecarlo-poker.herokuapp.com/](https://montecarlo-poker.herokuapp.com/).

Would love any feedback, pull requests, etc.

## Getting Started
Requirements: Python 3

Getting set up locally is simple. Once you've cloned the project:

Run `pip install requirements.txt`

Set up a local_settings.py file and drop it in the holdem/ folder where the settings.py file lives

```
# local_settings.py

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '[YOUR_SECRET_KEY]'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Relax throttling for testing
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100000/second',
        'user': '100000/second'
    }
}

```

Run `python manage.py migrate`
Run `python manage.py collectstatic`

## Running the tests
My goal with this project is to have 100% test coverage server-side.

`coverage run --source='.' manage.py test` runs tests

`coverage html` generates the coverage files

Built With
- Django
- Bootstrap
- Chart.js - Open source HTML5 charts

Author: Garrett Edel | [LinkedIn](https://www.linkedin.com/in/garrettedel/)

License: MIT License

Copyright (c) 2019 Garrett Edel

See LICENSE.txt file for details