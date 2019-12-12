from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime

def date_validator(value):
    now = timezone.now()
    if value < now:
        raise ValidationError('%(value)s should be greater than now', params={'value': value})