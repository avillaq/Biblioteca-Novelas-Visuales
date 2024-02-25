import re
import random
from datetime import datetime

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

# Pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from VNDisplay.Post import VN_Scraper
from VNDisplay.forms import PostFilterForm
from VNDisplay.models import Post, Category

scraper = VN_Scraper()

def home(request):
    posts = Post.objects.all()

    carousel_posts = random.sample(list(posts), 10)
    last_posts = posts.order_by('-id')[:32]

    return render(request, 'home.html', {'carousel_posts': carousel_posts, 
                                         'last_posts': last_posts})

def directory(request):

    posts = Post.objects.all()
    
    form = PostFilterForm(request.GET)
    if form.is_valid():
        field = form.cleaned_data["field"]
        order = form.cleaned_data["order"]
        category = form.cleaned_data["category"]
        year = form.cleaned_data["year"]

        if order == 'desc':
            field = '-' + field

        if category:
            posts = posts.filter(categories=category)

        if year:
            posts = posts.filter(date__year=year)

        # Ordena los posts por 'field'
        posts = posts.order_by(field)

        print(f"Form is valid: {form.cleaned_data}")
    else:
        form = PostFilterForm()
        posts = posts.order_by('-id')

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

    return render(request, 'directory.html', {'posts': posts, 'form': form})

def post_list(request):
    form = PostFilterForm(request.GET)
    posts = Post.objects.all()
    if form.is_valid():
        if form.cleaned_data['title']:
            posts = posts.filter(title__icontains=form.cleaned_data['title'])
        if form.cleaned_data['description']:
            posts = posts.filter(description__icontains=form.cleaned_data['description'])
    return render(request, 'directory.html', {'posts': posts, 'form': form})

def create_slug(full_url):
    match = re.search(r"/([\w-]+)\.html", full_url)
    if match:
        match = match.group(1)
    else:
        raise ValueError(f"Invalid URL: {full_url}")
    return match

def verify_new_posts():
    if not Post.objects.exists():  #IMPORTANT: If there are no posts in the database. IT WILL TAKE A FEW MINUTES 
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