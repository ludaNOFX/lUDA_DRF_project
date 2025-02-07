import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_luda_project.settings')


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
    }
)