from django.core.exceptions import ImproperlyConfigured
try:
    from django.utils import importlib
except ImportError:
    from haystack.utils import importlib


DEFAULT_ALIAS = 'default'


def import_class(path):
    path_bits = path.split('.')
    # Cut off the class name at the end.
    class_name = path_bits.pop()
    module_path = '.'.join(path_bits)
    module_itself = importlib.import_module(module_path)
    
    if not hasattr(module_itself, class_name):
        raise ImportError("The Python module '%s' has no '%s' class." % (module_path, class_name))
    
    return getattr(module_itself, class_name)


# Load the search backend.
def load_backend(full_backend_path):
    """
    Loads a backend for interacting with the search engine.
    
    Requires a ``backend_path``. It should be a string resembling a Python
    import path, pointing to a ``BaseEngine`` subclass. The built-in options
    available include::
    
      * haystack.backends.solr.SolrEngine
      * haystack.backends.xapian.XapianEngine (third-party)
      * haystack.backends.whoosh.WhooshEngine
      * haystack.backends.simple.SimpleEngine
    
    If you've implemented a custom backend, you can provide the path to
    your backend & matching ``Engine`` class. For example::
    
      ``myapp.search_backends.CustomSolrEngine``
    
    """
    path_bits = full_backend_path.split('.')
    
    if len(path_bits) < 2:
        raise ImproperlyConfigured("The provided backend '%s' is not a complete Python path to a BaseEngine subclass." % full_backend_path)
    
    return import_class(full_backend_path)


def load_router(full_router_path):
    """
    Loads a router for choosing which connection to use.
    
    Requires a ``full_router_path``. It should be a string resembling a Python
    import path, pointing to a ``Router`` class. The built-in options
    available include::
    
      * haystack.routers.DefaultRouter
    
    If you've implemented a custom backend, you can provide the path to
    your backend & matching ``Engine`` class. For example::
    
      ``myapp.search_routers.MasterSlaveRouter``
    
    """
    path_bits = full_router_path.split('.')
    
    if len(path_bits) < 2:
        raise ImproperlyConfigured("The provided router '%s' is not a complete Python path to a Router class." % full_router_path)
    
    return import_class(full_router_path)


class ConnectionHandler(object):
    def __init__(self, connections_info):
        self.connections_info = connections_info
        self._connections = {}
    
    def __getitem__(self, key):
        if key in self._connections:
            return self._connections[key]
        
        self._connections[key] = load_backend(key)
        return self._connections[key]


class ConnectionRouter(object):
    def __init__(self, routers_list=None):
        self.routers_list = routers_list
        self.routers = []
        
        if self.routers_list is None:
            self.routers_list = ['haystack.routers.DefaultRouter']
        
        for router_path in self.routers_list:
            router_class = load_router(router_path)
            self.routers.append(router_class())
    
    def for_action(self, action, index, model, **hints):
        for router in self.routers:
            if hasattr(router, action):
                action_callable = getattr(router, action)
                connection_to_use = action_callable(index, model, **hints)
                
                if connection_to_use is not None:
                    return connection_to_use
        
        # If we didn't find a router to handle it, use the default.
        return DEFAULT_ALIAS
    
    def for_write(self, index, model, **hints):
        return self.for_action('for_write', index, model, **hints)
    
    def for_read(self, index, model, **hints):
        return self.for_action('for_read', index, model, **hints)
