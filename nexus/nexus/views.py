from django.http import HttpResponse

def home_view(request):
    return HttpResponse("<h1>Essa é a home bar</h1>")