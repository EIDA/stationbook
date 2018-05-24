import sys
import os
import django
proj_path = '../stationbook/'
sys.path.append(proj_path)
os.chdir(proj_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stationbook.settings")
django.setup()

from book.fdsn.fdsn_manager import FdsnManager

if __name__ == '__main__':
    FdsnManager().process_fdsn()
