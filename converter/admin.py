from django.contrib import admin

# Register your models here.
from .models import Book, PurportPara, Theme, Shloka, Question


class BookAdmin(admin.ModelAdmin):
    # a list of displayed columns name.
    list_display = ['name', 'author']


class QuestionAdmin(admin.ModelAdmin):
    # a list of displayed columns name.
    list_display = ['number', 'para', 'text']


class PurportParaAdmin(admin.ModelAdmin):
    # a list of displayed columns name.
    list_display = ['shloka', 'number', 'text']


class ShlokaAdmin(admin.ModelAdmin):
    # a list of displayed columns name.
    list_display = ['book', 'chapter', 'number', 'text', 'translation']


admin.site.register(Book, BookAdmin)
admin.site.register(PurportPara, PurportParaAdmin)
admin.site.register(Theme)
admin.site.register(Shloka, ShlokaAdmin)
admin.site.register(Question, QuestionAdmin)
