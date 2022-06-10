from .views import ProgramAPI, BookAPI, CategoryAPI
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)
router.register('programs', ProgramAPI, basename='programs')
router.register('books', BookAPI, basename='books')
router.register('categories', CategoryAPI, basename='categories')

urlpatterns = router.urls