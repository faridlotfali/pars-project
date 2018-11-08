from django.contrib import admin
from .models import question,option
# Register your models here.

class OptionInline(admin.StackedInline):
    model = option
    extra = 2

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text',)
    inlines = [OptionInline]

admin.site.register(question,QuestionAdmin)
# admin.site.register(option)
