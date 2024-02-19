from django.shortcuts import render, redirect
from django.http import HttpResponse
from VNDisplay.Post import VN_Scraper, Post, Post_Android

scraper = VN_Scraper()
current_posts = []

# Create your views here.
#index view
def home(request):
    posts = scraper.get_section("inicio")
    global current_posts
    current_posts = posts

    return render(request, 'home.html', {'posts': posts})

def novel_detail(request, year, month, title):
    title = title.replace('/', '')
    url = f'http://www.visualnovelparapc.com/{year}/{month}/{title}.html'

    print(f"{len(current_posts)}")
    if len(current_posts) == 0:
        return redirect("home.html")

    post = None
    for p in current_posts:
        if p.full_url == url:
            post = p
            break

    post = scraper.get_post_detail(p)
    return render(request, 'novel_detail.html', {'post': post})

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