from .views import OauthAPI
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)
router.register('oauth', OauthAPI, basename='oauth')

urlpatterns = router.urls