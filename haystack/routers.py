from haystack.utils.loading import DEFAULT_ALIAS


class BaseRouter(object):
    # Reserved for future extension.
    pass


class DefaultRouter(BaseRouter):
    def for_read(self, index, model, **hints):
        return DEFAULT_ALIAS
    
    def for_write(self, index, model, **hints):
        return DEFAULT_ALIAS
    