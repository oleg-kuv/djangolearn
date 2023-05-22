from django.http import HttpResponse
from artickle.models import Artickle

def index (request):
    result = Artickle.objects.get(id=1)
    return HttpResponse(result)
