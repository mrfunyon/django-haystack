from haystack.constants import DEFAULT_ALIAS


class BaseRouter(object):
    # Reserved for future extension.
    pass


class DefaultRouter(BaseRouter):
    def for_read(self, index, model=None, **hints):
        return DEFAULT_ALIAS
    
    def for_write(self, index, model=None, **hints):
        return DEFAULT_ALIAS
    