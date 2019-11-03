from django.db import models
from django.conf import settings
from django.utils.text import slugify
from autoslug import AutoSlugField
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
class category(models.Model):
    parent_id = models.ForeignKey('self', null=True, on_delete=models.SET_NULL, blank = True)
    name = models.CharField('Category name', max_length=255, blank=False, unique=True)
    is_enabled = models.BooleanField('is enabled', default = True)
    slug = AutoSlugField(populate_from='name',unique=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f'{self.name}, if {self.parent_id} != None: {self.parent_id}'

    def get_absolute_url(self):
        return reverse('core:category', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = None
        super().save(*args, **kwargs)

class lot(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Lot''s owner', on_delete=models.PROTECT, null=True, related_name='lot_user')
    category_id = models.ForeignKey(category, verbose_name='Category', on_delete=models.SET_NULL, null=True, related_name='lot_category')
    name = models.CharField('Lot name', max_length=255, blank=False, unique=False)
    info = models.TextField('Additional information', blank=True)
    url = models.URLField(default='https://google.com')
    is_enabled = models.BooleanField('is enabled', default = True)
    image = models.ImageField(verbose_name='Picture',upload_to='product',null=True,blank=True)
    slug = AutoSlugField(populate_from='name',unique=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f'{self.name}, {self.category_id}, '

    def get_absolute_url(self):
        return reverse('lots:lot', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)