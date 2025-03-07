# Station Book

This repository is deployed at [orfeus-eu.org/stationbook](https://orfeus-eu.org/stationbook/).

## Quick start guide

1. Create env file with config using `cp src/stationbook/.env.sample src/stationbook/.env` and adjust as needed:

    ```bash
    SECRET_KEY='abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    DEBUG=False
    ALLOWED_HOSTS=.localhost,127.0.0.1,0.0.0.0
    DATABASE_URL=sqlite:////data/stationbook/db/db.sqlite3
    EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
    CACHE_BACKEND=django.core.cache.backends.locmem.LocMemCache
    CACHE_LOCATION='sb_cache'
    CACHE_TIME_SHORT=1800
    CACHE_TIME_MEDIUM=3600
    CACHE_TIME_LONG=43200
    SB_URL_BASE='stationbook/'
    CSRF_COOKIE_HTTPONLY = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    HCAPTCHA_SITEKEY=''
    HCAPTCHA_SECRET=''
    ```

1. Create the virtual environment and install dependencies:

    ```bash
    cd src/stationbook
    python3.11 -m venv env && source env/bin/activate && pip install --upgrade pip && pip install -r requirements.txt
    ```

1. Prepare the database migration and apply it:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

1. Create the super user:

    ```bash
    python manage.py createsuperuser
    ```

1. Load the fixtures into the database:

    ```bash
    python manage.py loaddata book.json
    ```

1. Create the cache table in the database

    ```bash
    python manage.py createcachetable
    ```

1. Run the test server:

    ```bash
    python manage.py runserver 0.0.0.0:8080
    ```

## Docker

```bash
# Build the image
docker build . -t stationbook:latest

# Run the container (replace PATH_TO_MEDIA and PATH_TO_DB accordingly)
docker run -d --restart always \
--user $(id -u):$(id -g) \
-p 8010:80 \
-v PATH_TO_MEDIA:/data/stationbook/media \
-v PATH_TO_DB:/data/stationbook/db \
--name stationbook \
stationbook:latest
```

## FDSN data synchronization

Below code can be used to synchronize with the EIDA nodes. EIDA nodes can be configured manually using admin panel or loaded from the fixtures.

```bash
python3 fdsn_sync.py
```

To automate the synchronization process, `/stationbook/src/stationbook/fdsn_sync.py` can be executed via crontab:

```bash
# min   hour    day     month   weekday command
0       *       *       *       *       cd /data/stationbook && python fdsn_sync.py
```
