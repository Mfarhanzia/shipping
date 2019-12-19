from django.contrib import admin
from .models import Order, Material, MaterialQuotations, ContainerPricing, CartOrder, CustomContainerPricing
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ('f_name','when_to_order','how_much_letter_of_credit','how_much_line_of_credit')
    list_filter = ('when_to_order',)
    list_display_links = ('f_name','when_to_order',)
    list_per_page = 50
    class Media:
        js = ('users/custom/custom_jquery.js',)
admin.site.register(Order, OrderAdmin)

admin.site.register(CartOrder)


class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    list_per_page = 50
admin.site.register(Material, MaterialAdmin)


class ContainerPricingAdmin(admin.ModelAdmin):
    
    list_display = ('pk', 'no_of_floors','variant',)
    list_display_links = ('no_of_floors','variant',)
    list_per_page = 50
admin.site.register(ContainerPricing, ContainerPricingAdmin)

class CustomContainerPricingAdmin(admin.ModelAdmin):
    list_display = ('pk','sqfeet_per_room',)
    list_display_links = ('pk','sqfeet_per_room',)
    list_per_page = 50

admin.site.register(CustomContainerPricing, CustomContainerPricingAdmin)


class MaterialQuotationsAdmin(admin.ModelAdmin):
    
    list_display = ('company_name',)
    list_display_links = ('company_name',)
    list_filter = ('company_name',)
    list_per_page = 50
admin.site.register(MaterialQuotations, MaterialQuotationsAdmin)




