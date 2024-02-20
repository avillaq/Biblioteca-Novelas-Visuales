import re
from datetime import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse
from VNDisplay.Post import VN_Scraper
from VNDisplay.models import Post, Category

scraper = VN_Scraper()
current_posts = []

def home(request):
    if not Post.objects.exists():
        posts = scraper.get_all_posts() 
        for post in reversed(posts):
            new_post = Post.objects.create(title=post.title, slug=create_slug(post.full_url), full_url=post.full_url, 
                                image_url=post.image_url, description=post.description, 
                                date=post.date)
            for label in post.labels:
                post_category = Category.objects.get(name=label)
                new_post.categories.add(post_category)

    else: 
        posts = scraper.get_section("inicio")  
        latest_post = Post.objects.latest('date') 
        for post in reversed(posts):

            # Convertir la cadena de texto a una fecha
            post_date = datetime.strptime(post.date, '%Y-%m-%d').date()
            #latest_post_date = datetime.strptime(str(latest_post.date), '%Y-%m-%d').date()
            if post_date >= latest_post.date and post.title != latest_post.title:  
                new_post = Post.objects.create(title=post.title, slug=create_slug(post.full_url), full_url=post.full_url, 
                                    image_url=post.image_url, description=post.description, 
                                    date=post.date)
                for label in post.labels:
                    post_category = Category.objects.get(name=label)
                    new_post.categories.add(post_category)

    posts = Post.objects.all().order_by('-date')
    return render(request, 'home.html', {'posts': posts})


def homes(request):
    posts = scraper.get_all_posts() # trae todos los posts de la pagina original

    posts = scraper.get_section("inicio") # trae todos los posts de la primera pagina (ya que tiene paginacion) de la seccion "inicio" de la pagina original

    #post = Post.objects.create(title=p.title, slug=create_slug(p.full_url), full_url=p.full_url, image_url=p.image_url, description=p.description, categories=p.labels, date=p.date)
    #Post.objects.all().delete()

    return render(request, 'home.html', {'posts': posts})


def create_slug(full_url):
    match = re.search(r"/([\w-]+)\.html", full_url)
    if match:
        match = match.group(1)
    else:
        raise ValueError(f"Invalid URL: {full_url}")
    return match

def delete_all(request):
    Post.objects.all().delete()
    return redirect("home.html")


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