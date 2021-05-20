from django.contrib import admin
from .models import Question,Theme,Shloka
# Register your models here.

admin.site.register(Question)
admin.site.register(Theme)
admin.site.register(Shloka)
# admin.site.register(Referance)