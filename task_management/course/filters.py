import django_filters
from .models import Author, Book, Category

class BookFilter(django_filters.FilterSet):
    class Meta:
        model = Book
        fields = []
    
    name = django_filters.CharFilter(
        field_name= 'name',
        lookup_expr='icontains'
    )
    author = django_filters.CharFilter(
        field_name='author__full_name',
        lookup_expr='icontains'
    )
    category = django_filters.CharFilter(
        field_name='categories__name',
        lookup_expr='icontains'
    )