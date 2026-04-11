from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def districts(request):
    return HttpResponse("districts")