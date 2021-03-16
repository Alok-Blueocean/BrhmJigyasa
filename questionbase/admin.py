from django.contrib import admin
from .models import Answer,Question,Tag,SubTag,Referance
# Register your models here.
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Tag)
admin.site.register(SubTag)
admin.site.register(Referance)