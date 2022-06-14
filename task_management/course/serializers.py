from dataclasses import fields
from pyexpat import model
from statistics import mode
from turtle import pd
from rest_framework import serializers
from .models import Price, Program, Book, Author, Category
from utils.views import exceptions

class BaseAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = [
            'uid',
            'full_name',
            'dob'
        ]

class BaseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'name',
            'description',
        ]

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = [
            'name',
        ]

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = [
            'program',
            'from_date',
            'to_date'
        ]
class BookSerializer(serializers.ModelSerializer):
    uid = serializers.CharField()
    name = serializers.CharField()
    # def validate_data(self):
    author = BaseAuthorSerializer(read_only = True)
    categories = BaseCategorySerializer(read_only = True, many=True)
    class Meta:
        model = Book
        fields = [
            'uid',
            'name',
            'public_at',
            'author',
            'categories',
        ]

class CategorySerializer(serializers.ModelSerializer):

    def validate(self, data):
        if not data.get('name', None):
            raise exceptions.InvalidArgumentException()
        if not data['description']:
            raise exceptions.InvalidArgumentException(message="aa")
        return data

    class Meta:
        model = Category
        fields = [
            'name',
            'description'
        ]

