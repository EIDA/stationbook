# Station Book
This repository is deployed at [orfeus-eu.org/stationbook](https://orfeus-eu.org/stationbook/).
## Quick start guide
1. Create the .env configuration file in `/src/stationbook/.env`. Example test server configuration:
    ```
    SECRET_KEY='abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    DEBUG=True
    ALLOWED_HOSTS=.localhost,127.0.0.1
    DATABASE_URL=sqlite:////data/stationbook/db/db.sqlite3
    EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
    CACHE_BACKEND=django.core.cache.backends.db.DatabaseCache
    CACHE_LOCATION='sb_cache'
    CACHE_TIME_SHORT=1800
    CACHE_TIME_MEDIUM=3600
    CACHE_TIME_LONG=43200
    SB_URL_BASE=''
    CSRF_COOKIE_HTTPONLY = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    HCAPTCHA_SITEKEY=''
    HCAPTCHA_SECRET=''

    ```
    * SECRET_KEY should be a 50-characters long string of random characters from the following set: `abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)`
    * `CACHE_BACKEND` can be set to:
        * `django.core.cache.backends.memcached.MemcachedCache` with location `127.0.0.1:11211` (default for python-memcached)
        * `django.core.cache.backends.locmem.LocMemCache` local-memory cache backend
        * `django.core.cache.backends.filebased.FileBasedCache` with location e.g. `/data/sb_cache/`
        * `django.core.cache.backends.db.DatabaseCache` with location e.g. `sb_cache_table`
        * `django.core.cache.backends.dummy.DummyCache` can be used during development
    * `CACHE_TIME_SHORT`, `CACHE_TIME_MEDIUM` and `CACHE_TIME_LONG` are timers (in seconds) used for cache validation assigned to pages depending on how often their content changes
    * `SB_URL_BASE` allows adding a URL prefix to all Station Book URLs
1. Make sure SQLite is configured as the default database in `src/stationbook/stationbook/settings.py`
1. Create the virtual environment:
    ```
    [usr@host src]$ python -m venv env
    ```
1. Activate the virtual environment:
    ```
    [usr@host src]$ source env/bin/activate
    ```
1. Install the dependencies:
    ```
    (env) [usr@host src]$ pip install -r requirements.txt
    ```
1. Go to the root directory:
    ```
    (env) [usr@host stationbook]$ cd stationbook/
    ```
1. Prepare the database migration and apply it:
    ```
    (env) [usr@host stationbook]$ python manage.py makemigrations
    (env) [usr@host stationbook]$ python manage.py migrate
    ```
1. Create the super user:
    ```
    (env) [usr@host stationbook]$ python manage.py createsuperuser
    ```
1. Load the fixtures into the database:
    ```
    (env) [usr@host stationbook]$ python manage.py loaddata book.json
    ```
1. Create the cache table in the database
    ```
    (env) [usr@host stationbook]$ python manage.py createcachetable
    ```
1. Run the test server:
    ```
    (env) [usr@host stationbook]$ python manage.py runserver 0.0.0.0:8080
    ```
1. To clear the cache:
    ```
    (env) [usr@host stationbook]$ python manage.py shell
    >>> from django.core.cache import cache
    >>> cache.clear()
    ```

## Docker
1. Build and run the images
    ```
    (env) [usr@host src]$ docker-compose -p 'stationbook' up -d --no-deps --build
    ```
1. Migrating the database, loading the fixtures, creating super user and synchronizing with the FDSN can be done after connecting to the image containing the Station Book code.
    ```
    [usr@host ~]$ docker exec -it <CONTAINER ID> sh
    ```

## FDSN data synchronization
Below code can be used to synchronize with the EIDA nodes. EIDA nodes can be configured manually using admin panel or loaded from the fixtures.
```
(env) [usr@host stationbook]$ python manage.py shell
>>> from book.fdsn.fdsn_manager import FdsnManager
>>> FdsnManager().process_fdsn()
```
To automate the synchronization process, `/stationbook/src/stationbook/fdsn_sync.py` can be executed via crontab:
```
# min   hour    day     month   weekday command
0       *       *       *       *       cd /data/stationbook && python fdsn_sync.py
```
