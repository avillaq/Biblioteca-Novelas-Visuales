from django.shortcuts import render
from django.http import HttpResponse
from Post import VN_Scraper, Post, Post_Android


# Create your views here.
#index view
def home(request):
    return HttpResponse("Hello, world. You're at the VNDisplay index.")

def completo(request):
    return HttpResponse("Hello, world. You're at the VNDisplay completo.")

def allages(request):
    return HttpResponse("Hello, world. You're at the VNDisplay allages.")

def yuri(request):
    return HttpResponse("Hello, world. You're at the VNDisplay yuri.")

def otome(request):
    return HttpResponse("Hello, world. You're at the VNDisplay otome.")

def eroge(request):
    return HttpResponse("Hello, world. You're at the VNDisplay eroge.")