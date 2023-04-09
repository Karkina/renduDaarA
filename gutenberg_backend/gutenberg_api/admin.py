from django.contrib import admin

# Register your models here.
from gutenberg_api.models import BookIndexModel, BookModel, GraphJaccard

admin.site.register(BookModel)
admin.site.register(BookIndexModel)
admin.site.register(GraphJaccard)