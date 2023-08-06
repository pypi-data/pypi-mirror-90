from rest_framework.routers import DefaultRouter
from bluedot_rest_framework import import_string

ConfigsView = import_string('configs.views')
router = DefaultRouter(trailing_slash=False)

router.register(r'configs', ConfigsView,
                basename='configs')

urlpatterns = router.urls
