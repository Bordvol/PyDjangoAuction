from django.contrib import admin
from users.models import CustomUser
from auctions.models import auction, bet, discussion


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'name', 'surname', 'phone', 'is_staff', 'is_active', 'date_joined', 'last_login')
    list_display_links = ('id', 'email' )
    search_fields = ('email','name','surname','phone')
    list_editable = ('is_active',)
    list_filter = ('is_staff', 'is_active')
