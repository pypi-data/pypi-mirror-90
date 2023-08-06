# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ci_ynh', 'ci_ynh.migrations']

package_data = \
{'': ['*']}

install_requires = \
['bx_py_utils',
 'django',
 'django-axes',
 'django-huey-monitor',
 'django-redis',
 'django_ynh',
 'gunicorn',
 'huey',
 'psycopg2-binary']

setup_kwargs = {
    'name': 'ci-ynh',
    'version': '0.1.0a0',
    'description': 'CI for YunoHost to test YunoHost packages ;)',
    'long_description': "# ci_ynh for YunoHost\n\n[![Integration level](https://dash.yunohost.org/integration/ci_ynh.svg)](https://dash.yunohost.org/appci/app/ci_ynh) ![](https://ci-apps.yunohost.org/ci/badges/ci_ynh.status.svg) ![](https://ci-apps.yunohost.org/ci/badges/ci_ynh.maintain.svg)\n[![Install ci_ynh with YunoHost](https://install-app.yunohost.org/install-with-yunohost.svg)](https://install-app.yunohost.org/?app=ci_ynh)\n\n> *This package allows you to install ci_ynh quickly and simply on a YunoHost server.\nIf you don't have YunoHost, please consult [the guide](https://yunohost.org/#/install) to learn how to install it.*\n\n**Experimental and currently not working ;)**\n\nPull requests welcome ;)\n\nDiscuss: https://forum.yunohost.org/t/ci-ynh-package-check-as-yunohost-app-using-django/13894\n\n## Overview\n\n[ci_ynh](https://github.comYunoHost-Apps/ci_ynh) CI to check YunoHost packages on self hosted YunoHost instance, using Python/Django.\n\n\n\n## Links\n\n * Report a bugs: https://github.com/YunoHost-Apps/ci_ynh\n * YunoHost website: https://yunohost.org/\n\n---\n\n# Developer info\n\n## package installation / debugging\n\nPlease send your pull request to https://github.com/YunoHost-Apps/ci_ynh\n\nTry 'main' branch, e.g.:\n```bash\nsudo yunohost app install https://github.com/YunoHost-Apps/ci_ynh/tree/master --debug\nor\nsudo yunohost app upgrade ci_ynh -u https://github.com/YunoHost-Apps/ci_ynh/tree/master --debug\n```\n\nTry 'testing' branch, e.g.:\n```bash\nsudo yunohost app install https://github.com/YunoHost-Apps/ci_ynh/tree/testing --debug\nor\nsudo yunohost app upgrade ci_ynh -u https://github.com/YunoHost-Apps/ci_ynh/tree/testing --debug\n```\n\nTo remove call e.g.:\n```bash\nsudo yunohost app remove ci_ynh\n```\n\nBackup / remove / restore cycle, e.g.:\n```bash\nyunohost backup create --apps ci_ynh\nyunohost backup list\narchives:\n  - ci_ynh-pre-upgrade1\n  - 20201223-163434\nyunohost app remove ci_ynh\nyunohost backup restore 20201223-163434 --apps ci_ynh\n```\n\nDebug installation, e.g.:\n```bash\nroot@yunohost:~# ls -la /var/www/ci_ynh/\ntotal 18\ndrwxr-xr-x 4 root root 4 Dec  8 08:36 .\ndrwxr-xr-x 6 root root 6 Dec  8 08:36 ..\ndrwxr-xr-x 2 root root 2 Dec  8 08:36 media\ndrwxr-xr-x 7 root root 8 Dec  8 08:40 static\n\nroot@yunohost:~# ls -la /opt/yunohost/ci_ynh/\ntotal 58\ndrwxr-xr-x 5 ci_ynh ci_ynh   11 Dec  8 08:39 .\ndrwxr-xr-x 3 root        root           3 Dec  8 08:36 ..\n-rw-r--r-- 1 ci_ynh ci_ynh  460 Dec  8 08:39 gunicorn.conf.py\n-rw-r--r-- 1 ci_ynh ci_ynh    0 Dec  8 08:39 local_settings.py\n-rwxr-xr-x 1 ci_ynh ci_ynh  274 Dec  8 08:39 manage.py\n-rw-r--r-- 1 ci_ynh ci_ynh  171 Dec  8 08:39 secret.txt\ndrwxr-xr-x 6 ci_ynh ci_ynh    6 Dec  8 08:37 venv\n-rw-r--r-- 1 ci_ynh ci_ynh  115 Dec  8 08:39 wsgi.py\n-rw-r--r-- 1 ci_ynh ci_ynh 4737 Dec  8 08:39 settings.py\n\nroot@yunohost:~# cd /opt/yunohost/ci_ynh/\nroot@yunohost:/opt/yunohost/ci_ynh# source venv/bin/activate\n(venv) root@yunohost:/opt/yunohost/ci_ynh# ./manage.py check\nci_ynh v0.8.2 (Django v2.2.17)\nDJANGO_SETTINGS_MODULE='settings'\nPROJECT_PATH:/opt/yunohost/ci_ynh/venv/lib/python3.7/site-packages\nBASE_PATH:/opt/yunohost/ci_ynh\nSystem check identified no issues (0 silenced).\n\nroot@yunohost:~# tail -f /var/log/ci_ynh/ci_ynh.log\nroot@yunohost:~# cat /etc/systemd/system/ci_ynh.service\n\nroot@yunohost:~# systemctl reload-or-restart ci_ynh\nroot@yunohost:~# journalctl --unit=ci_ynh --follow\n```\n\n## local test\n\nFor quicker developing of ci_ynh in the context of YunoHost app,\nit's possible to run the Django developer server with the settings\nand urls made for YunoHost installation.\n\ne.g.:\n```bash\n~$ git clone https://github.com/YunoHost-Apps/ci_ynh.git\n~$ cd ci_ynh/\n~/ci_ynh$ make\ninstall-poetry         install or update poetry\ninstall                install ci_ynh via poetry\nupdate                 update the sources and installation\nlocal-test             Run local_test.py to run ci_ynh locally\n~/ci_ynh$ make install-poetry\n~/ci_ynh$ make install\n~/ci_ynh$ make local-test\n```\n\nNotes:\n\n* SQlite database will be used\n* A super user with username `test` and password `test` is created\n* The page is available under `http://127.0.0.1:8000/app_path/`\n",
    'author': 'JensDiemer',
    'author_email': 'git@jensdiemer.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/YunoHost-Apps/ci_ynh',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0.0',
}


setup(**setup_kwargs)
