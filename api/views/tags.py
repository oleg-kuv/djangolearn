from rest_framework import viewsets
from api.serializers import TagSerializer
from blog.models import Tag


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
