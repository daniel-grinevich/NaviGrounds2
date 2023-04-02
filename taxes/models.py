import uuid
from django.db import models
import datetime
from django.contrib.auth import get_user_model

# Create your models here.
class Status(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class PaymentMethod(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Entry(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    title = models.CharField(
        max_length=150,
        null=False,
        unique=False,
        verbose_name='entry title',
        help_text='format: required, max characters: 150'
    )
    description = models.CharField(
        max_length=255, 
        null=False,
        unique=False,
        verbose_name='entry description',
        help_text="Enter a brief description of what you bought."
    )
    memo = models.CharField(
        max_length=255, 
        null=True,
        unique=False,
        verbose_name='memo',
        help_text="Not required, memo of the purchase."
    )
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    total_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        null=False,
        unique=False,
        default=0.00,
        verbose_name='total price',
        help_text="Required, max digits 10.",
    )
    tax_year = models.IntegerField(
        default=datetime.date.today().year,
        null=False,
        unique=False,
        verbose_name='tax year',
        help_text='required, automatically added'
    )
    purchase_date = models.DateField(
        default=datetime.date.today,
        verbose_name='purchase date',
        null=False,
        unique=False,
        help_text='required, automatically added',
    )
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    receipt_img = models.ImageField(upload_to='entry_images', null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Item(models.Model):
    name = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    entry = models.ForeignKey(Entry, on_delete=models.PROTECT)

    def __str__(self):
        return self.name
    


