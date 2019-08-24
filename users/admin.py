from django.contrib import admin
from .models import SpecialUser, SpecialUserLog, User, Dealer, Photo, WaterMark, EmailList 

# Register your models here.
class SpecialUserLogInline(admin.TabularInline):
    model = SpecialUserLog

class SpecialUserAdmin(admin.ModelAdmin):
    list_display = ("pk","email","company_name","user_type")
    list_display_links = ("pk","email",)
    list_filter = ("user_type",)
    inlines = [SpecialUserLogInline]
    list_per_page = 50
    
admin.site.register(SpecialUser, SpecialUserAdmin)

admin.site.register(Photo)

class WaterMarkAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # if there's already an entry, do not allow adding
        count = WaterMark.objects.all().count()
        if count == 0:
            return True
        return False

admin.site.register(WaterMark,WaterMarkAdmin)


class EmailListAdmin(admin.ModelAdmin):
    list_display = ['email']     
    list_per_page = 50
admin.site.register(EmailList,EmailListAdmin)

class UserAdmin(admin.ModelAdmin):
    list_display = ['email']
    readonly_fields = ('password',) 
    list_per_page = 50
admin.site.register(User, UserAdmin)

class DealerAdmin(admin.ModelAdmin):
 
    list_display = ['email']
    readonly_fields = ('password','content_page_link',)
    list_per_page = 50 
admin.site.register(Dealer,DealerAdmin)

# class SpecialUserLogAdmin(admin.ModelAdmin):
#     list_display = ("pk","specialuser",)
#     list_display_links = ("pk","specialuser",)

# admin.site.register(SpecialUserLog, SpecialUserLogAdmin)
