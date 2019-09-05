from django.contrib import admin
from .models import User, Photo, WaterMark, EmailList, SpecUser

# Register your models here.

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

class SpecUserAdmin(admin.ModelAdmin):
     
    list_display = ['email','user_type']
    readonly_fields = ('password',)
    list_filter = ['user_type']
    list_per_page = 50 
admin.site.register(SpecUser,SpecUserAdmin)

