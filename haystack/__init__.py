import logging
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from haystack.utils import loading


__author__ = 'Daniel Lindsley'
__version__ = (2, 0, 0, 'alpha')
__all__ = ['backend']


# Setup default logging.
log = logging.getLogger('haystack')
stream = logging.StreamHandler()
stream.setLevel(logging.INFO)
log.addHandler(stream)


# Help people clean up from 1.X.
if hasattr(settings, 'HAYSTACK_SITECONF'):
    raise ImproperlyConfigured('The HAYSTACK_SITECONF setting is no longer used & can be removed.')
if hasattr(settings, 'HAYSTACK_SEARCH_ENGINE'):
    raise ImproperlyConfigured('The HAYSTACK_SEARCH_ENGINE setting has been replaced with HAYSTACK_CONNECTIONS.')
if hasattr(settings, 'HAYSTACK_ENABLE_REGISTRATIONS'):
    raise ImproperlyConfigured('The HAYSTACK_ENABLE_REGISTRATIONS setting is no longer used & can be removed.')


# Check the 2.X+ bits.
if not hasattr(settings, 'HAYSTACK_CONNECTIONS'):
    raise ImproperlyConfigured('The HAYSTACK_CONNECTIONS setting is required.')
if loading.DEFAULT_ALIAS not in settings.HAYSTACK_CONNECTIONS:
    raise ImproperlyConfigured("The default alias '%s' must be included in the HAYSTACK_CONNECTIONS setting." % loading.DEFAULT_ALIAS)
for alias, connection in settings.HAYSTACK_CONNECTIONS.items():
    if 'ENGINE' not in connection:
        raise ImproperlyConfigured("You must specify a 'ENGINE' for connection '%s'" % alias)

# Load the connections.
connections = loading.ConnectionHandler(settings.HAYSTACK_CONNECTIONS)

# Load the router(s).
router = loading.ConnectionRouter()

if hasattr(settings, 'HAYSTACK_ROUTERS'):
    if not isinstance(settings.HAYSTACK_ROUTERS, (list, tuple)):
        raise ImproperlyConfigured("The HAYSTACK_ROUTERS setting must be either a list or tuple.")
    
    router = loading.ConnectionRouter(settings.HAYSTACK_ROUTERS)
