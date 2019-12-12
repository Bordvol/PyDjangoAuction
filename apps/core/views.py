from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from lots import models as lots_models
from users import models as users_models
from auctions import models as auctions_models
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View, TemplateView, ListView, DetailView, FormView
from core.forms import NewLotForm, NewAuctionForm, NewBetForm, NewCommentForm
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, JsonResponse
from decimal import Decimal
from django import forms
from django.contrib import messages
from django.utils import timezone


class IndexView(ListView):
    template_name = 'core/index.html'
    queryset = auctions_models.auction.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        auctions_qs = auctions_models.auction.objects.filter(is_enabled=True, is_finished=False)

        search = self.request.GET.get('search')
        if search:
            lot_qs = lots_models.lot.objects.all()
            lot_qs = lot_qs.filter(name__icontains=search)
            auctions_qs = auctions_qs.filter(lot_id__in=[lot for lot in lot_qs])

        paginator = Paginator(auctions_qs.order_by('-pk'), 5)
        page = self.request.GET.get('page')

        try:
            auction_list = paginator.page(page)
        except PageNotAnInteger:
            auction_list = paginator.page(1)
        except EmptyPage:
            auction_list = paginator.page(paginator.num_pages)

        context['auctions_count'] = auctions_models.auction.objects.filter(is_enabled=True).count()
        context['active_auctions_count'] = auctions_models.auction.objects.filter(is_enabled=True, is_finished=False).count()
        context['auctions_list'] = auction_list
        return context


class AuctionListView(ListView):
    template_name = 'core/auctions_list.html'
    queryset = auctions_models.auction.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        auctions_qs = auctions_models.auction.objects.filter(is_enabled=True)

        paginator = Paginator(auctions_qs.order_by('-pk'), 5)
        page = self.request.GET.get('page')

        try:
            auction_list = paginator.page(page)
        except PageNotAnInteger:
            auction_list = paginator.page(1)
        except EmptyPage:
            auction_list = paginator.page(paginator.num_pages)

        context['auctions_count'] = auctions_models.auction.objects.filter(is_enabled=True).count()
        context['active_auctions_count'] = auctions_models.auction.objects.filter(is_enabled=True, is_finished=False).count()
        context['auctions_list'] = auction_list
        return context


class MyAuctionListView(ListView):
    template_name = 'core/my_auctions_list.html'
    queryset = auctions_models.auction.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        auctions_qs = auctions_models.auction.objects.filter(user_id = self.request.user)

        paginator = Paginator(auctions_qs.order_by('-pk'), 5)
        page = self.request.GET.get('page')

        try:
            auction_list = paginator.page(page)
        except PageNotAnInteger:
            auction_list = paginator.page(1)
        except EmptyPage:
            auction_list = paginator.page(paginator.num_pages)

        context['auctions_count'] = auctions_models.auction.objects.filter(user_id = self.request.user).count()
        context['active_auctions_count'] = auctions_models.auction.objects.filter(is_enabled=True,
                                                                                  is_finished=False).count()
        context['auctions_list'] = auction_list
        return context


class MyLotListView(ListView):
    template_name = 'core/my_lots_list.html'
    queryset = lots_models.lot.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lots_qs = lots_models.lot.objects.filter(user_id = self.request.user)

        paginator = Paginator(lots_qs.order_by('-pk'), 5)
        page = self.request.GET.get('page')

        try:
            lot_list = paginator.page(page)
        except PageNotAnInteger:
            lot_list = paginator.page(1)
        except EmptyPage:
            lot_list = paginator.page(paginator.num_pages)

        context['lots_count'] = lots_models.lot.objects.filter(user_id = self.request.user).count()
        context['active_lots_count'] = lots_models.lot.objects.filter(is_enabled=True, user_id = self.request.user).count()
        context['lots_list'] = lot_list
        return context


class AuctionView(ListView):
    template_name = 'core/auction.html'
    queryset = auctions_models.auction.objects.all()

    def get_context_data(self, **kwargs):
        pk_ = self.kwargs.get("pk")
        context = super().get_context_data(**kwargs)
        auction_qs = auctions_models.auction.objects.filter(pk=pk_).first()
        context['auction'] = auction_qs

        if not auction_qs.is_blind:
            context['bets_list'] = auctions_models.bet.objects.filter(auction_id=pk_).order_by('-pk')

        context['bets_count'] = auctions_models.bet.objects.filter(auction_id=pk_).count()
        context['comments_list'] = auctions_models.discussion.objects.filter(auction_id=pk_).order_by('-pk')
        context['comments_count'] = auctions_models.discussion.objects.filter(auction_id=pk_).count()
        return context


class LotView(ListView):
    template_name = 'core/lot.html'
    queryset = lots_models.lot.objects.all()

    def get_context_data(self, **kwargs):
        pk_ = self.kwargs.get("pk")
        context = super().get_context_data(**kwargs)
        lot_qs = lots_models.lot.objects.filter(pk=pk_).first()
        context['lot'] = lot_qs
        context['auctions_list'] = auctions_models.auction.objects.filter(lot_id=lot_qs).filter(is_finished=False).order_by('-pk')
        context['auctions_count'] = auctions_models.auction.objects.filter(lot_id=lot_qs).filter(is_finished=False).count()
        return context


class NewLotView(FormView):
    template_name = 'core/new_lot.html'
    form_class = NewLotForm
    success_url = reverse_lazy('core:index')
    user = get_user_model()

    def form_valid(self, form):
        obj = form.save(commit=False)

        user = self.request.user
        user_to_save = users_models.CustomUser()
        user_to_save.id = user.id
        obj.user_id = user_to_save

        obj.save()
        return super().form_valid(form)


class NewAuctionView(FormView):
    template_name = 'core/new_auction.html'
    form_class = NewAuctionForm
    success_url = reverse_lazy('core:index')
    user = get_user_model()

    def form_valid(self, form):
        obj = form.save(commit=False)

        user = self.request.user
        user_to_save = users_models.CustomUser()
        user_to_save.id = user.id
        obj.user_id = user_to_save

        obj.save()
        return super().form_valid(form)


class NewBetView(FormView):
    form_class = NewBetForm
    success_url = reverse_lazy('core:index')
    user = get_user_model()

    def post(self, request, *args, **kwargs):

        error_count = 0
        system_messages = messages.get_messages(request)
        for message in system_messages:
            pass
        system_messages.used = True

        bet = auctions_models.bet()
        bet.amount = request.POST.get("new_bet_input")

        pk  = request.POST.get("pk")
        auction_to_save = get_object_or_404(auctions_models.auction, pk=pk)

        bet.auction_id = auction_to_save

        user_to_save = self.request.user
        bet.user_id = user_to_save

        if auction_to_save.blitz_price:
            if auction_to_save.action_type_id == 0:
                if (Decimal(bet.amount) <= auction_to_save.blitz_price):
                    auction_to_save.winner = user_to_save
                    auction_to_save.is_finished = True
                    messages.success(request, 'You are the winner! Congrats!')
            else:
                if (Decimal(bet.amount) >= auction_to_save.blitz_price):
                    auction_to_save.winner = user_to_save
                    auction_to_save.is_finished = True
                    messages.success(request, 'You are the winner! Congrats!')

        #validations
        if auction_to_save.is_blind == False:
            if auction_to_save.action_type_id == 0:
                if Decimal(bet.amount) > auction_to_save.get_min_next_bet():
                    error_count += 1
                    messages.success(request, ('Bet should be equal or less than ' + str(auction_to_save.get_min_next_bet())))
            else:
                if Decimal(bet.amount) < auction_to_save.get_min_next_bet():
                    error_count += 1
                    messages.success(request, ('Bet should be equal or greater than ' + str(auction_to_save.get_min_next_bet())))

        if error_count == 0:
            auction_to_save.current_price = bet.amount
            bet.save()
            auction_to_save.save()

        return redirect('core:auction' , pk)


class NewCommentView(FormView):
    form_class = NewCommentForm
    success_url = reverse_lazy('core:index')
    user = get_user_model()

    def post(self, request, *args, **kwargs):

        discussion = auctions_models.discussion()
        discussion.message = request.POST.get("new_comment_input")

        pk  = request.POST.get("pk")
        auction_to_save = get_object_or_404(auctions_models.auction, pk=pk)
        discussion.auction_id = auction_to_save

        user_to_save = self.request.user
        discussion.user_id = user_to_save

        discussion.save()
        return redirect('core:auction' , pk)


class CheckView(FormView):
    form_class = NewBetForm
    success_url = reverse_lazy('core:index')

    def post(self, request, *args, **kwargs):
        now = timezone.now()
        auctions_qs = auctions_models.auction.objects.filter(is_finished=False)
        for auction in auctions_qs:
            if auction.bid_end_datetime <= now:

                auction.is_finished = True
                bets_count = auctions_models.bet.objects.filter(auction_id=auction).count()
                if bets_count > 0:
                    bet = auctions_models.bet.objects.filter(auction_id=auction).order_by('-amount', 'bet_date')[0]
                    print (bet)
                    print (bet.amount)
                    auction.winner = bet.user_id
                auction.save()

        return redirect('core:index')