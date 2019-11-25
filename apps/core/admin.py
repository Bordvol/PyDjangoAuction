from django.contrib import admin
from lots.models import lot, category
from auctions.models import auction, bet, discussion
from users.models import CustomUser

# Register your models here.CustomUser
admin.site.register(lot)
admin.site.register(category)
admin.site.register(auction)
admin.site.register(bet)
admin.site.register(discussion)
#admin.site.register(CustomUser)
