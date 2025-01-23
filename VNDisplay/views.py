import random
from datetime import timedelta

from django.shortcuts import get_object_or_404, render, redirect

# Pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from VNDisplay.Post import VN_Blogger
from VNDisplay.forms import PostFilterForm
from VNDisplay.models import Post, Category, Android_Post, Type

blogger = VN_Blogger()

def home(request):
    posts = Post.objects.all()

    simple_num = 10 if len(posts) > 10 else len(posts)

    carousel_posts = random.sample(list(posts), simple_num)
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
            posts = posts.filter(publication_date__year=year)

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

def novel_detail(request, id_post):
    post = get_object_or_404(Post,
                            id_post=id_post)

    screenshot_urls = post.get_screenshot_urls()
    specifications = post.get_specifications()

    return render(request, 'novel_detail.html', {'post': post, 'screenshot_urls': screenshot_urls, 'specifications': specifications})

def update_novels(request):
    query = request.GET.get('novel-type')
    if query == "pc":
        verify_new_posts()
        return redirect('/')
    elif query == "kirikiroid2":
        verify_new_android_posts("kirikiroid2", blogger.get_kirikiroid2_section)
        verify_kirikiroid2_emulator()
        return redirect('/android/kirikiroid2')
    elif query == "apk":
        verify_new_android_posts("apk", blogger.get_apk_section)
        return redirect('/android/apk')


######################################### Auxiliary functions #########################################

def verify_new_posts():
    if not Post.objects.exists():  #IMPORTANT: If there are no posts in the database. 
        posts = blogger.get_all_posts() #IT WILL TAKE A FEW MINUTES TO GET ALL THE POSTS
        for post in reversed(posts):
            try:
                new_post, created = Post.objects.get_or_create(
                                    id_post=post.id_post, 
                                    defaults={
                                        "title": post.title, 
                                        "full_url": post.full_url,
                                        "synopsis": post.synopsis,
                                        "cover_url": post.cover_url,
                                        "publication_date": post.publication_date,
                                        "update_date": post.update_date
                                    }
                                )
                if created:
                    new_post.set_screenshot_urls(post.screenshot_urls)
                    new_post.set_specifications(post.specifications)
                    new_post.save()

                    for label in post.labels:
                        post_category = Category.objects.get(name=label)
                        new_post.categories.add(post_category)
            except Exception as e:
                print(f"Error creating post {post.id_post}: {str(e)}")
                continue

    else: 
        latest_post = Post.objects.latest('publication_date')
        latest_post_date = latest_post.publication_date - timedelta(days=1) 
        posts = blogger.get_section(
                                category="inicio",
                                start_index=1, 
                                max_results=100,
                                published_min=latest_post_date)  
        
        for post in reversed(posts):
            new_post, created = Post.objects.get_or_create(
                                id_post=post.id_post, 
                                defaults={
                                    "title": post.title, 
                                    "full_url": post.full_url,
                                    "synopsis": post.synopsis,
                                    "cover_url": post.cover_url,
                                    "publication_date": post.publication_date,
                                    "update_date": post.update_date
                                }
                            )
            if created:
                new_post.set_screenshot_urls(post.screenshot_urls)
                new_post.set_specifications(post.specifications)
                new_post.save()

                for label in post.labels:
                    post_category = Category.objects.get(name=label)
                    new_post.categories.add(post_category)
        

def verify_new_android_posts(type_name, blogger_function):
    android_posts = blogger_function() 
    post_type = Type.objects.get(name=type_name)
    for post in reversed(android_posts):
        new_post, created = Android_Post.objects.get_or_create(
                            title=post.title, 
                            type=post_type,
                            defaults={
                                "full_url": post.full_url,
                                "cover_url": post.cover_url
                            }
                        )

def verify_kirikiroid2_emulator():
    Type.objects.filter(name="kirikiroid2").update(resource=blogger.get_kirikiroid2_emulator())



