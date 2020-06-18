from django.contrib import admin
from .models import User,  EmailList, SpecUser, UserPreferences, ModelImages, ModelsInfo
# Register your models here.


class EmailListAdmin(admin.ModelAdmin):
    list_display = ['email']     
    list_per_page = 50

admin.site.register(EmailList,EmailListAdmin)


# class CartOrderAdmin(admin.TabularInline):
#     model = CartOrder
#     list_display = ['user','orderitems']
    

class UserAdmin(admin.ModelAdmin):
    list_display = ['email']
    readonly_fields = ('password',) 
    # inlines = [CartOrderAdmin]
    list_per_page = 50

admin.site.register(User, UserAdmin)


class SpecUserAdmin(admin.ModelAdmin):
    list_display = ['email','user_type','content_permission','home_permission']
    readonly_fields = ('password',)
    list_filter = ['user_type','content_permission','home_permission']
    list_per_page = 50
    # inlines = [CartOrderAdmin]
admin.site.register(SpecUser,SpecUserAdmin)


class UserPreferencesAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserPreferences,UserPreferencesAdmin)


class ModelImagesAdmin(admin.TabularInline):
    model = ModelImages


class ModelsInfoAdmin(admin.ModelAdmin):
    list_display = ['model_name']
    inlines = [ModelImagesAdmin]


admin.site.register(ModelsInfo, ModelsInfoAdmin)

