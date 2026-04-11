from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.

def index(request):
    if request.htmx:
        return render(request, "cotton/partials/index_partial.html")
    return render(request, 'index.html')

def dashboard(request):
    if request.htmx:
        return render(request, "cotton/partials/index_partial.html")
    return render(request, 'index.html')