from django import forms
from lots.models import lot


class NewLotForm(forms.ModelForm):
    user_id = 1#forms.CharField(label='Имя', max_length=128)
    category_id = 1#forms.CharField(max_length=255, widget=forms.Textarea({'rows': 2, 'cols': 20}), required=False)
    name = forms.CharField(label='lot_name', max_length=128)
    info = forms.CharField(label='lot_info', max_length=4000)
    url = forms.CharField(label='lot_url', max_length=4000)
    is_enabled = 1

    class Meta:
        model = lot
        fields = '__all__'