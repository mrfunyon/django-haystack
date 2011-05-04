from haystack.utils.loading import DEFAULT_ALIAS


class BaseRouter(object):
    # Set as None to indicate use all indexes/models.
    valid_indexes = None


class DefaultRouter(BaseRouter):
    def for_read(self, index, model, **hints):
        return DEFAULT_ALIAS
    
    def for_write(self, index, model, **hints):
        return DEFAULT_ALIAS
    