from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from.models import CustomUser,Blog
# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display=('username','email','first_name','last_name','bio','profile','twitter','linkedin','instagram','portfolio')
    
admin.site.register(CustomUser,CustomUserAdmin)

class BlogAdmin(admin.ModelAdmin):
    list_display=('title','is_draft_pub','category','created_time')
    
    

    
admin.site.register(Blog,BlogAdmin)





