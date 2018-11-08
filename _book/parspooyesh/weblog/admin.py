from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.
from .models import Comment,slider
from .models import Post,Profile,SiteSettings


admin.site.site_header = "ParsPooyesh Admin"
admin.site.site_title = "ParsPooyesh Admin Portal"
admin.site.index_title = "Welcome to ParsPooyesh Portal"

# class QuestionAdmin(admin.ModelAdmin):
#     fields = ['pub_date', 'post_text']

class ChoiceInline(admin.StackedInline):
    model = Comment
    extra = 2

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
    ('lock',{'fields': ['post_text']}),
    ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]

class Site_SettingAdmin(admin.ModelAdmin):
    list_display = ('key_name', 'key_value')

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(slider)
admin.site.register(Profile)
admin.site.register(SiteSettings,Site_SettingAdmin)

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)    