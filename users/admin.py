from django.contrib import admin
from .models import SpecialUser, SpecialUserLog, Photo, WaterMark 

# Register your models here.
class SpecialUserLogInline(admin.TabularInline):
    model = SpecialUserLog

class SpecialUserAdmin(admin.ModelAdmin):
    list_display = ("pk","company_name","email","user_type")
    list_filter = ("user_type",)
    inlines = [SpecialUserLogInline]
    
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


# class SpecialUserLogAdmin(admin.ModelAdmin):
#     list_display = ("pk","specialuser",)
#     list_display_links = ("pk","specialuser",)

    

# admin.site.register(SpecialUserLog, SpecialUserLogAdmin)