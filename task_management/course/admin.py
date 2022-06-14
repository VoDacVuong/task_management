from django.contrib import admin
from . models import Program, Price, Book, Author, Category
# Register your models here.

admin.site.register(Program)
admin.site.register(Price)
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Category)

