from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product
from django.utils import timezone


def home(request):
    products = Product.objects
    return render(request, 'products/home.html', {'products': products})


@login_required(login_url='/acounts/signup')
def create(request):
    if request.method == 'POST':
        print(request.POST)
        print(request.FILES)
        print(request.user)
        if _all_fields_filled(request):
            product = Product()
            product = _input_request2product(request, product)
            product.save()
            return redirect(f'/products/{product.id}')
        else:
            return render(request, 'products/create.html', {'error': 'All fields are required.'})
    else:
        return render(request, 'products/create.html')


def _all_fields_filled(request):
    return request.POST['title'] and request.POST['body'] and request.POST['url'] and request.FILES['icon'] and request.FILES['image']


def _input_request2product(request, product):
    product.title = request.POST['title']
    product.body = request.POST['body']
    if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
        product.url = request.POST['url']
    else:
        product.url = 'http://' + request.POST['url']
    product.icon = request.FILES['icon']
    product.image = request.FILES['image']
    product.pub_date = timezone.datetime.now()
    product.hunter = request.user
    return product


def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/detail.html', {'product': product})


@login_required(login_url='/acounts/signup')
def upvote(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        product.votes_total += 1
        product.save()
        return redirect(f'/products/{product_id}')
