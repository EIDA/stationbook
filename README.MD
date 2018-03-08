# Quick start guide
1. Create the .env configuration file in `/src/stationbook/.env`.
Example test server configuration:
    ```
    SECRET_KEY=''
    DEBUG=True
    ALLOWED_HOSTS=.localhost,127.0.0.1
    DATABASE_URL=sqlite:///db.sqlite3
    DATABASE_ENGINE='django.db.backends.postgresql'
    DATABASE_NAME='postgres'
    DATABASE_USER='postgres'
    DATABASE_HOST='db'
    DATABASE_PORT=5432
    EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
    ```
    SECRET_KEY should be a 50-characters long string of random characters from the following set: `abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)`
1. Create the virtual environment:
    ```
    [usr@host src]$ python3 -m venv env
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
    (env) [usr@host stationbook]$ python3 manage.py makemigrations
    (env) [usr@host stationbook]$ python3 manage.py migrate
    ```
1. Create the super user:
    ```
    (env) [usr@host stationbook]$ python3 manage.py createsuperuser
    ```
1. Load the fixtures into the database:
    ```
    (env) [usr@host stationbook]$ python3 manage.py loaddata book.json
    ```
1. Run the test server:
    ```
    (env) [usr@host stationbook]$ python3 manage.py runserver 0.0.0.0:8080
    ```
# FDSN data synchronization
Below code can be used to synchronize with the EIDA nodes. EIDA nodes can be configured manually using admin panel or loaded from the fixtures.
```
(env) [usr@host stationbook]$ python3 manage.py shell
>>> from book.fdsn.fdsn_manager import FdsnManager
>>> FdsnManager().process_fdsn()
```
# Logs
Tail can be used to follow the app logs:
```
[usr@host stationbook]$ tail -f logs/station_book.log
```