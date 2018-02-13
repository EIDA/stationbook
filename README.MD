# Quick start guide
```
[usr@host src]$ python3 -m venv env
[usr@host src]$ source env/bin/activate
(env) [usr@host src]$ pip install -r requirements.txt
(env) [usr@host stationbook]$ cd stationbook/
(env) [usr@host stationbook]$ python3 manage.py makemigrations
(env) [usr@host stationbook]$ python3 manage.py migrate
(env) [usr@host stationbook]$ python3 manage.py createsuperuser
(env) [usr@host stationbook]$ python3 manage.py runserver 0.0.0.0:8080
```
