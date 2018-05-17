# /git/stationbook/src/.env
    DB_NAME=stationbook
    DB_USER=admin
    DB_PASS=passwd
    DB_SERVICE=postgres
    DB_PORT=5432

# /git/stationbook/src/stationbook/.env
    SECRET_KEY='#ps1ib&=v%zsgzi5q*qp-ei*b1bg19dxv&861m@4@x+2ww6nx^'
    DEBUG=True
    ALLOWED_HOSTS=.localhost,127.0.0.1
    DATABASE_URL=sqlite:///db.sqlite3
    DATABASE_ENGINE='django.db.backends.postgresql'
    DATABASE_HOST='postgres'
    DATABASE_NAME='stationbook'
    DATABASE_USER='admin'
    DATABASE_PASS='passwd'
    DATABASE_PORT=5432
    EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
    CACHE_BACKEND=django.core.cache.backends.db.DatabaseCache
    CACHE_LOCATION='sb_cache'
    CACHE_TIME_SHORT=1800
    CACHE_TIME_MEDIUM=3600
    CACHE_TIME_LONG=43200
    SB_URL_BASE='sb2/'

# Cache backends
* `django.core.cache.backends.dummy.DummyCache` (development)
* `django.core.cache.backends.db.DatabaseCache`
* `django.core.cache.backends.memcached.MemcachedCache`