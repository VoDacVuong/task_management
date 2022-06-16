# from .views import UserAPI
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)
# router.register('users', UserAPI, basename='users')

urlpatterns = router.urls