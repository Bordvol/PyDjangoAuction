from django.contrib import admin
from lots.models import lot, category
from auctions.models import auction, bet

# Register your models here.
admin.site.register(lot)
admin.site.register(category)
admin.site.register(auction)
admin.site.register(bet)
