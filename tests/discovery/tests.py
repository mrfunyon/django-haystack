from django.conf import settings
from django.test import TestCase
from haystack import connections, connection_router
from haystack.utils.loading import UnifiedIndex
from discovery.search_indexes import FooIndex, BarIndex


class ManualSiteRegistrationTestCase(TestCase):
    def test_registrations(self):
        old_ui = connection_router.get_unified_index()
        connection_router._index = UnifiedIndex()
        ui = connection_router.get_unified_index()
        self.assertEqual(len(ui.get_indexed_models()), 2)
        
        ui.build(indexes=[FooIndex()])
        
        self.assertEqual(len(ui.get_indexed_models()), 1)
        
        ui.build(indexes=[])
        
        self.assertEqual(len(ui.get_indexed_models()), 0)
        connection_router._index = old_ui


class AutoSiteRegistrationTestCase(TestCase):
    def test_registrations(self):
        old_ui = connection_router.get_unified_index()
        connection_router._index = UnifiedIndex()
        ui = connection_router.get_unified_index()
        self.assertEqual(len(ui.get_indexed_models()), 2)
        
        # Test exclusions.
        ui.excluded_indexes = ['discovery.search_indexes.BarIndex']
        ui.build()
        
        self.assertEqual(len(ui.get_indexed_models()), 1)
        
        ui.excluded_indexes = ['discovery.search_indexes.BarIndex', 'discovery.search_indexes.FooIndex']
        ui.build()
        
        self.assertEqual(len(ui.get_indexed_models()), 0)
        connection_router._index = old_ui
