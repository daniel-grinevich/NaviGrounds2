from django.contrib import admin
from .models import Status, Category, PaymentMethod, Entry, Item

# Register your models here.
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name','description')
    model = Status

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','description')
    model = Category

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('name','description')
    model = PaymentMethod

class EntryAdmin(admin.ModelAdmin):
    list_display = ('title','user','tax_year','status','payment_method','updated_at')
    list_filter = ('status__name','tax_year','created_at')
    model = Entry

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name','cost','entry')
    model = Item

admin.site.register(Status, StatusAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(PaymentMethod, PaymentAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Item, ItemAdmin)