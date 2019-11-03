from django.db import models
from lots import models as lot_models
from django.conf import settings

# Create your models here.
AUCTION_TYPE_CHOISE = (
    (0, 'decrease_price'),
    (1, 'increase_price'),
)


class auction(models.Model):
    action_type_id = models.IntegerField('Auction type',choices=AUCTION_TYPE_CHOISE, default = 0)
    lot_id = models.ForeignKey(lot_models.lot, verbose_name='Lot', on_delete=models.PROTECT, null=False, related_name='auction_lot')
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Auction''s owner', on_delete=models.PROTECT, null=False, related_name='auction_user')
    starting_price = models.FloatField('Starting price', max_length=10, default = 0)
    current_price = models.FloatField('Current price', max_length=10, default = 0)
    min_bet_step = models.FloatField('Minimum bet step', max_length=10, default = 0)
    blitz_price = models.FloatField('Blitz price', max_length=10, default = 0)
    bid_end_datetime = models.DateTimeField('Finish on')
    is_blind = models.BooleanField('is blind', default = False)
    is_enabled = models.BooleanField('is enabled', default = True)
    is_finished = models.BooleanField('is finished', default = False)
    winner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Winner of the auction', on_delete=models.PROTECT, null=True, related_name='auction_winner_user')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class bet(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=False, related_name='bet_user')
    auction_id  = models.ForeignKey(auction, on_delete=models.PROTECT, null=False, related_name='bet_auction')
    amount = models.FloatField()
    bet_date = models.DateTimeField()