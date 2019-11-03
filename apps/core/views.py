from django.shortcuts import render
from lots import models as lot_models
from auctions import models as auction_models
from django.shortcuts import get_object_or_404


def index(request):
    ctx = {}
    ctx['auction_list'] = auction_models.auction.objects.all()[:3]
    return render(request, 'core/index.html', ctx)


def auction_list(request):
    ctx = {}
    ctx['auction_list'] = auction_models.auction.objects.all()
    return render(request, 'core/auction_list.html', ctx)


def auction(request, pk):
    ctx = {}
    product = auction_models.auction.objects.filter(pk=pk).first()
    if product:
        ctx['auction'] = auction
    return render(request, 'core/auction.html', ctx)

def lot(request, pk):
    ctx = {}
    product = lot_models.lot.objects.filter(pk=pk).first()
    if product:
        ctx['lot'] = lot
    return render(request, 'core/lot.html', ctx)

def category_list(request):
    ctx = {}

    category_list = list()
    for category in lot_models.category.objects.all():
        category_list.append({
            'url': category.get_absolute_url(),
            'name': category.name,
        })
    ctx['category_list'] = category_list
    return render(request, 'core/category_list.html', ctx)


def category(request, slug):
    ctx = {}
    category = lot_models.category.filter(slug=slug).first()
    if category:
        ctx['category'] = category.name
      #  ctx['product_list'] = category.product_set.all()
    return render(request, 'core/category.html', ctx)
