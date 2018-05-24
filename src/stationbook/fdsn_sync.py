import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stationbook.settings")
django.setup()

from book.fdsn.fdsn_manager import FdsnManager

if __name__ == '__main__':
    FdsnManager().process_fdsn()
