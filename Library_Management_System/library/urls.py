from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import LibrarianViewSet, UserViewSet

router = DefaultRouter()
router.register(r'librarian', LibrarianViewSet, basename='librarian')
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path('api/', include(router.urls)),
]
# https://chatgpt.com/c/675b27d1-301c-800c-806c-4cbf9c9bd337