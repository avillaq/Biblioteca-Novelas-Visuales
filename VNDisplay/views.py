import re
import random
from datetime import datetime

from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse

# Pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from VNDisplay.Post import VN_Scraper
from VNDisplay.forms import PostFilterForm
from VNDisplay.models import Post, Category, Android_Post, Type, PostDetail

scraper = VN_Scraper()

def home(request):
    posts = Post.objects.all()

    carousel_posts = random.sample(list(posts), 10)
    last_posts = posts.order_by('-id')[:32]

    return render(request, 'home.html', {'carousel_posts': carousel_posts, 
                                         'last_posts': last_posts})

def directory(request):

    posts = Post.objects.all()
    filtered = ""

    form = PostFilterForm(request.GET)
    if form.is_valid():
        field = form.cleaned_data["field"]
        order = form.cleaned_data["order"]
        category = form.cleaned_data["category"] 
        year = form.cleaned_data["year"]

        filtered = "&field=" + field + "&order=" + order + "&category=" + (str(category.id) if category else "") + "&year=" + str(year)

        if order == 'desc':
            field = '-' + field

        if category:
            posts = posts.filter(categories=category)

        if year:
            posts = posts.filter(date__year=year)

        posts = posts.order_by(field)


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

    return render(request, 'directory.html', {'posts': posts, 'form': form, 'filtered': filtered})

def search(request):
    query = request.GET.get('q')
    if not query or query.strip() == '' or len(query) < 3 or len(query) > 50:
        return render(request, 'search.html',{'posts': None, 'query': query})
    posts = Post.objects.filter(title__icontains=query)
    apk_posts = Android_Post.objects.filter(title__icontains=query, type__name="apk")
    kirikiroid2_posts = Android_Post.objects.filter(title__icontains=query, type__name="kirikiroid2")
    return render(request, 'search.html', {'posts': posts, 'apk_posts': apk_posts, 'kirikiroid2_posts': kirikiroid2_posts, 'query': query})

def android(request):
    return render(request, 'android.html')

def android_apk(request):
    android_posts = Android_Post.objects.filter(type__name="apk").order_by('-id')
    return render(request, 'android_apk.html', {'android_posts': android_posts})

def android_kirikiroid2(request):
    kirikiroid2_emualtor = Type.objects.get(name="kirikiroid2").resource
    android_posts = Android_Post.objects.filter(type__name="kirikiroid2").order_by('-id')
    return render(request, 'android_kirikiroid2.html', {'android_posts': android_posts, 'emulador': kirikiroid2_emualtor})

def novel_detail(request, year, month, day, title):
    post = get_object_or_404(Post,
                            slug=title,
                            date__year=year,
                            date__month=month,
                            date__day=day)
    post_detail = PostDetail.objects.get(post=post)

    synopsis = post_detail.synopsis
    image_urls = post_detail.get_image_urls()
    features = post_detail.get_features()

    return render(request, 'novel_detail.html', {'post': post, 'synopsis': synopsis, 'image_urls': image_urls, 'features': features})

def update_novels(request):
    query = request.GET.get('novel-type')
    if query == "pc":
        verify_new_posts()
        return redirect('/')
    else:
        verify_new_android_posts("kirikiroid2", scraper.get_kirikiroid2_section)
        verify_kirikiroid2_emulator()
        return redirect('/directorio')


######################################### Auxiliary functions #########################################

def verify_new_posts():
    if not Post.objects.exists():  #IMPORTANT: If there are no posts in the database. 
        posts = scraper.get_all_posts() #IT WILL TAKE A FEW MINUTES TO SCRAPE ALL THE POSTS
        for post in reversed(posts):
            new_post = Post.objects.create(title=post.title, slug=create_slug(post.full_url), full_url=post.full_url, 
                                image_url=post.image_url, description=post.description, 
                                date=post.date)
            for label in post.labels:
                post_category = Category.objects.get(name=label)
                new_post.categories.add(post_category)
            
            #create_post_detail(new_post)  

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

                create_post_detail(new_post)

def create_slug(full_url):
    match = re.search(r"/([\w-]+)\.html", full_url)
    if match:
        match = match.group(1)
    else:
        raise ValueError(f"Invalid URL: {full_url}")
    return match

def create_post_detail(post):
    title, main_image, synopsis, screenshots, features = scraper.get_post_detail(post)
    post_detail = PostDetail.objects.create(post=post, synopsis=synopsis)
    post_detail.set_image_urls(screenshots)
    post_detail.set_features(features)
    post_detail.save()
    

def verify_new_android_posts(type_name, scraper_function):
    posts = Android_Post.objects.filter(type__name=type_name)
    android_posts = scraper_function() 
    if not posts:
        post_type = Type.objects.get(name=type_name)
        for post in reversed(android_posts):
            Android_Post.objects.create(title=post.title, full_url=post.full_url, 
                                    image_url=post.image_url, type=post_type)
    else: 
        total = posts.count()
        if total < len(android_posts):
            difference = len(android_posts) - total
            new_posts = android_posts[:difference]
            post_type = Type.objects.get(name=type_name)
            for post in reversed(new_posts):
                Android_Post.objects.create(title=post.title, full_url=post.full_url, 
                                    image_url=post.image_url, type=post_type)

def verify_kirikiroid2_emulator():
    Type.objects.filter(name="kirikiroid2").update(resource=scraper.get_kirikiroid2_emulator())



