from django.contrib import admin
from .models import Order
# Register your models here.

class OrderAdmin(admin.ModelAdmin):

    # fields = (
    #     'letter_of_credit',('line_of_credit',('zipcode')),
    # )

    list_display = ('f_name','when_to_order','how_much_letter_of_credit','how_much_line_of_credit')
    list_filter = ('when_to_order',)
    list_display_links = ('f_name','when_to_order',)
    class Media:
        js = ('users/custom/custom_jquery.js',)

admin.site.register(Order, OrderAdmin)