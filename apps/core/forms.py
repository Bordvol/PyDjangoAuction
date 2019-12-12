from django import forms
from lots.models import lot
from auctions.models import auction, bet, discussion
from core.validators import date_validator
from decimal import Decimal

class NewLotForm(forms.ModelForm):

    class Meta:
        model = lot
        fields = ('category_id', 'name', 'info', 'url', 'image')


class NewAuctionForm(forms.ModelForm):

    bid_end_datetime = forms.DateTimeField(label='bid end datetime',  validators=[date_validator])

    class Meta:
        model = auction
        fields = ('action_type_id', 'lot_id', 'starting_price', 'min_bet_step', 'blitz_price', 'bid_end_datetime', 'is_blind')#'__all__'

    def clean_starting_price(self):
        starting_price = self.cleaned_data["starting_price"]
        if starting_price <= 0:
            raise forms.ValidationError('Starting price should be greater than 0')
        return starting_price

    def clean_min_bet_step(self):
        min_bet_step = self.cleaned_data["min_bet_step"]
        if min_bet_step <= 0:
            raise forms.ValidationError('Minimum bet step should be greater than 0')
        return min_bet_step

    def clean(self):
        cleaned_data = super(NewAuctionForm, self).clean()

        blitz_price = cleaned_data.get("blitz_price")
        starting_price = cleaned_data.get("starting_price")
        action_type_id = cleaned_data.get("action_type_id")

        if blitz_price:
            if (action_type_id == 0)&(blitz_price >= starting_price):
                raise forms.ValidationError('In case of decrease auction blitz price should be less than starting price')
            if (action_type_id == 1)&(blitz_price <= starting_price):
                raise forms.ValidationError('In case of increase auction blitz price should be greater than starting price')


class NewBetForm(forms.ModelForm):
     amount = forms.DecimalField

     class Meta:
         model = bet
         fields = '__all__'

     def clean_amount(self):
         amount =self.cleaned_data["amount"]


class NewCommentForm(forms.ModelForm):
    class Meta:
        model = discussion
        fields = ('message',)