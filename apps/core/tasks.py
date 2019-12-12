#from app.celery import app
from celery import shared_task
from auctions import models as auctions_models
from django.utils import timezone

@app.task
def finish_auctions():
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

