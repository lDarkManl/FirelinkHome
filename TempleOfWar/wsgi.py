#-*- coding: utf-8 -*-
import os
import sys
import platform
#путь к проекту, там где manage.py
sys.path.insert(0, '/home/c/cp79068/FirelinkHome/public_html/TempleOfWar')
#путь к фреймворку, там где settings.py
sys.path.insert(0, '/home/c/cp79068/FirelinkHome/public_html/TempleOfWar/TempleOfWar')

sys.path.insert(0, '/home/c/cp79068/FirelinkHome/public_html/venv/lib/python3.6/site-packages')
os.environ["DJANGO_SETTINGS_MODULE"] = "TempleOfWar.settings"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()