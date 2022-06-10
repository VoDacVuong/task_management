from django.db import models
import uuid
# Create your models here.

class Program(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.name}'

class Price(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='price_program')
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()

    def __str__(self):
        return f'{self.program} - from:{self.from_date} - to:{self.to_date}'

class Order(models.Model):
    state = models.CharField(max_length=20)
    items = models.ManyToManyField(Price)
#---------------------------------------

class Book(models.Model):
    uid = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False, unique=True
    )
    name = models.CharField(max_length=200)
    public_at = models.DateField()
    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='book_author')
    categories = models.ManyToManyField('Category', related_name='book_categories')

    def __str__(self):
        return self.name

class Author(models.Model):
    uid = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False, unique=True
    )
    full_name = models.CharField(max_length=200)
    dob = models.DateField()

    def __str__(self):
        return self.full_name


class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    def __str__(self):
        return self.name 