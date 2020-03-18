"""
WSGI config for app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

if os.environ.get('DJANGO_DEBUG', False):  # You can use django.conf
    # settings.DEBUG
    import ptvsd
    ptvsd.enable_attach(address=('0.0.0.0', 8888))
    ptvsd.wait_for_attach()  # We can remove this line it gives you trouble,
    # but it's good to know if the debugger started or not
    # blocking the execution for a while :-)

application = get_wsgi_application()
