from django.http import HttpResponse

def index (request):
    host = request.META['HTTP_HOST']
    ua = request.META['HTTP_USER_AGENT']
    path = request.path
    return HttpResponse(f"""<pre>
Hello!
Host: {host}
Path: {path}
User-agent: {ua}
</pre>""")

def somepage (request):
    return HttpResponse("Somepage...")
