from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from lots import models as lots_models
from auctions import models as auctions_models
from django.shortcuts import get_object_or_404
from django.views.generic import View, TemplateView, ListView, DetailView, FormView
from core.forms import NewLotForm


class IndexView(TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['auctions_list'] = auctions_models.auction.objects.all()[:3]
        return context


class AuctionListView(ListView):
    template_name = 'core/auctions_list.html'
    queryset = auctions_models.auction.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        auction_qs = auctions_models.auction.objects.all()
        context['auctions_list'] = auction_qs
        return context

class AuctionView(ListView):
    template_name = 'core/auction.html'
    queryset = auctions_models.auction.objects.all()

    def get_context_data(self, **kwargs):
        pk_ = self.kwargs.get("pk")
        print (pk_)
        context = super().get_context_data(**kwargs)
        auction_qs = auctions_models.auction.objects.filter(pk=pk_).first()
        context['auction'] = auction_qs
        context['bets_list'] = auctions_models.bet.objects.filter(auction_id=pk_).all()
        return context

class NewLotView(FormView):
    template_name = 'core/new_lot.html'
    form_class = NewLotForm
  #  success_url = reverse_lazy('index')
    success_url = reverse_lazy('core:index')
   # fields = ('category_id', 'name', 'info', 'url', )

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

#class AuctionView(DetailView):
#    template_name = 'core/auction.html'
#    model = auctions_models.auction
#    context['auctions_list']

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
