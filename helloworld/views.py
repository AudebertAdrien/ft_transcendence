from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, CHAKIB est une trompette ou pas!")
