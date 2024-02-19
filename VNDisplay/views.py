import re
from django.shortcuts import render, redirect
from django.http import HttpResponse
from VNDisplay.Post import VN_Scraper
from VNDisplay.models import Post

scraper = VN_Scraper()
current_posts = []


def home(request):
    posts = scraper.get_section("inicio")[0:1]
    p = posts[0]
    
   
    post = Post(title=p.title, slug=create_slug(p.full_url), full_url=p.full_url, image_url=p.image_url, description=p.description, categories=p.labels, date=p.date)
    post.save()

    return render(request, 'home.html', {'posts': posts})


def create_slug(full_url):
    match = re.search(r"/([\w-]+)\.html", full_url)
    if match:
        match = match.group(1)
    else:
        raise ValueError(f"Invalid URL: {full_url}")
    return match


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