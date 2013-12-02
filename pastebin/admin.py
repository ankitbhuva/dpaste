import models
from django.contrib import admin
from django.contrib.auth.models import User

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title", )}
    exclude = ('author', )

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()

class CodePasteAdmin(admin.ModelAdmin):
	prepopulated_fields= {"title": ("title",), "name": ("name", )}
#	exclude = ('name', )
	
	def save_model(self, request, obj, form, change):
		obj.name = request.name
		obj.save()

admin.site.register(models.Post, PostAdmin)
admin.site.register(models.CodePaste, CodePasteAdmin)
