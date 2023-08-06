from rest_framework.routers import DefaultRouter
from bluedot_rest_framework import import_string

ConfigurationView = import_string('configuration.views')
router = DefaultRouter(trailing_slash=False)

router.register(r'configuration', ConfigurationView,
                basename='configuration')

urlpatterns = router.urls
