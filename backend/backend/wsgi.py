"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os, sys

# add the hellodjango project path into the sys.path
sys.path.append('/home/app/quick/backend')  # 添加你的项目绝对路径
# sys.path.append('/sdb/pyweb/djcode/website')


# add the virtualenv site-packages path to the sys.path
sys.path.append('/root/.local/share/virtualenvs/backend-7r4-iFNX/lib/python3.8/site-packages')  # 添加你虚拟环境包绝对路径
# sys.path.append('/sdb/pyweb/djcode/lib/python2.7/site-packages')


# poiting to the project settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

from django.core.wsgi import get_wsgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = get_wsgi_application()
