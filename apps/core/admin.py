from django.contrib import admin
from lots.models import lot, category
from auctions.models import auction, bet, discussion


admin.site.register(category)
admin.site.register(bet)
admin.site.register(discussion)


class BetInline(admin.TabularInline):
    model = bet
    extra = 0
    fields = ('user_id', 'amount')

@admin.register(auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = ('id', 'lot_id', 'action_type_id', 'starting_price', 'current_price', 'created_at', 'bid_end_datetime', 'is_enabled', 'is_finished')
    list_display_links = ('id', 'lot_id' )
    search_fields = ('lot_id','user_id','winner',)
    list_editable = ('is_enabled',)
    list_filter = ('is_blind', 'is_enabled', 'is_finished')

    inlines = (BetInline,)


@admin.register(lot)
class LotAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_id', 'name', 'url', 'is_enabled')
    list_display_links = ('id', 'name' )
    search_fields = ('name',)
    list_editable = ('is_enabled',)
    list_filter = ('is_enabled',)

