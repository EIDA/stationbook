# Quick start guide
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
Tail can be used to follow the sync status:
```
tail -f src/stationbook/logs/station_book.log
```