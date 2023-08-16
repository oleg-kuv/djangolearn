from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers

# from api.views.postapi import PostAPIView
from api.views.posts import *
from api.views.tags import *
from api.views.users import *

router = routers.SimpleRouter()
router.register(r'posts', PostViewSet)
router.register(r'tags', TagViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('blog/', include(router.urls))
]

urlpatterns = format_suffix_patterns(urlpatterns)
