import re
from datetime import datetime

from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse

# Pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from VNDisplay.Post import VN_Scraper
from VNDisplay.models import Post, Category

scraper = VN_Scraper()

def home(request):
    verify_new_posts()

    posts = Post.objects.all().order_by('-id')[:32]

    return render(request, 'home.html', {'posts': posts})

def directory(request):
    verify_new_posts()

    posts = Post.objects.all().order_by('-id')

    # Pagination with 3 posts per page
    paginator = Paginator(posts, 32)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request, 'directory.html', {'posts': posts})


def create_slug(full_url):
    match = re.search(r"/([\w-]+)\.html", full_url)
    if match:
        match = match.group(1)
    else:
        raise ValueError(f"Invalid URL: {full_url}")
    return match

def verify_new_posts():
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
        latest_post = Post.objects.latest('id')
        for post in reversed(posts):
            post_date = datetime.strptime(post.date, '%Y-%m-%d').date()
            if post_date > latest_post.date:
                new_post = Post.objects.create(title=post.title, slug=create_slug(post.full_url), full_url=post.full_url, 
                                    image_url=post.image_url, description=post.description, 
                                    date=post.date)
                for label in post.labels:
                    post_category = Category.objects.get(name=label)
                    new_post.categories.add(post_category)

def novel_detail(request, year, month, day, title):
    #url = f'http://www.visualnovelparapc.com/{year}/{month}/{title}.html'

    p = get_object_or_404(Post,
                            slug=title,
                            date__year=year,
                            date__month=month,
                            date__day=day)

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