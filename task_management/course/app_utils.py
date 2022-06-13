from turtle import pd
from unicodedata import name
from .models import Book, Author, Category
from utils import messages, exceptions

def get_book(uid):
    try:
        book = Book.objects.get(uid=uid)
        return book
    except Exception as exception:
        raise exceptions.InvalidArgumentException(message=messages.BOOK_NOT_FOUND)

def get_author(uid):
    try:
        author = Author.objects.get(pk=uid)
        return author
    except Exception as exception:
        raise exceptions.InvalidArgumentException(message=messages.AUTHOR_NOT_FOUND)

def get_category(pk):
    try:
        category = Category.objects.filter(pk=pk).first()
        return category
    except Exception as exception:
        raise exceptions.InvalidArgumentException(message=messages.CATEGORY_NOT_FOUND)

def update_category_by_dict(category, update_category_dict = {}):
    for key, value in update_category_dict.items():
        setattr(category, key, value)

    category.save()
    return category

def create_book_by_dict(create_book_dict = {}):
    book = Book.objects.create(
        name = create_book_dict.get('name'),
        public_at = create_book_dict.get('public_at'),
        author = get_author(uid = create_book_dict.get('author')),
        # categories = get_category(pk = create_book_dict.get('categories'))
    )
    
    book.categories.add(get_category(pk = create_book_dict.get('categories')))
    # import pdb;pdb.set_trace()
    return book

def create_category_by_dict(create_category_dict = {}):
    category = Category.objects.create(
        name = create_category_dict.get('name'),
        description = create_category_dict.get('description')
    )
    return category

def update_book_by_dict(book, update_book_dict = {}):
    try:
        for key, value in update_book_dict.items():
            if key == 'categories':
                book.categories.set(value)
                continue
            setattr(book, key, value)
        book.save()
        return book
    except Exception as exception:
        raise exceptions.InvalidArgumentException()
