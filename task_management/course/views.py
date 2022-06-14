from datetime import datetime
from .models import Book, Category, Program, Price
from rest_framework.decorators import action
from .serializers import ProgramSerializer, PriceSerializer, BookSerializer, CategorySerializer
from .filters import BookFilter
from utils.views import AbstractView, query_debugger, paginate_data
from utils import exceptions, messages
from course import app_utils as course_utils
import io
from django.http import FileResponse, HttpRequest, HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from drf_yasg.utils import swagger_auto_schema
from .swagger_params import(
   book_matrix_swagger_params,
)
# Create your models here.

class ProgramAPI(AbstractView):
    @action(methods=['POST'], url_path='matrix', detail=False)
    def matrix_program(self, request):
        programs = Price.objects.prefetch_related('program').all()
        response_data = PriceSerializer(programs, many=True).data
        return self.response_handler.handle(data=response_data)

class CategoryAPI(AbstractView):

    category_fields = [
        'name',
        'description',
    ]

    @query_debugger
    @action(methods=['POST'], url_path='create', detail=False)
    def create_category(self, request):
        try:
            data = self.request_handler.handle(request)
            create_category_dict = {
                k: data.get_body_value(k, None) for k in self.category_fields if data.get_body_value(k) is not None
            }
            category_serializer = CategorySerializer(data=create_category_dict)
            category_serializer.is_valid()

            course_utils.create_category_by_dict(
                create_category_dict = create_category_dict
            )
            return self.response_handler.handle(category_serializer.data)
        except Exception as exception:
            return self.exception_handler.handle(exception)

    @query_debugger
    @action(methods=['POST'], url_path='matrix', detail=False)
    def matrix_categories(self, request):
        try:
            categories = Category.objects.all()
            response_data = CategorySerializer(categories, many = True).data
            response_by_page = paginate_data(request, response_data)
            return self.response_handler.handle(response_by_page)
        except Exception as exception:
            return self.exception_handler.handle(exception)

    @query_debugger
    @action(methods=['POST'], url_path='update', detail=False)
    def update_category(self, request):
        try:
            data = self.request_handler.handle(request)
            pk_category = data.get_body_value('pk')
            category = course_utils.get_category(pk=pk_category)
            update_category_dict = {
                k : data.get_body_value(k, None) for k in self.category_fields if data.get_body_value is not None
            }
            category_new = course_utils.update_category_by_dict(
                category=category,
                update_category_dict = update_category_dict
            )
            response_data = CategorySerializer(category_new).data
            return self.response_handler.handle(response_data)
        except Exception as exception:
            return self.exception_handler.handle(exception)

class BookAPI(AbstractView):
    serializer_class = BookSerializer
    book_fields = [
        'name',
        'public_at',
        'author',
        'categories'
    ]
    @query_debugger
    @action(methods=['POST'], url_path='matrix', detail=False)
    def matrix_book(self, request):
        try:
            data = self.request_handler.handle(request)
            data_dict = dict()

            for field in BookFilter.base_filters:
                value = data.get_body_value(key=field)
                data_dict.setdefault(field, value)

            books = Book.objects.select_related('author')
            filtered_book = BookFilter(data_dict, books).qs
            response_data = BookSerializer(filtered_book, many = True).data
            response_by_page = paginate_data(request, response_data)
            return self.response_handler.handle(data=response_by_page)

        except Exception as exception:
            return self.exception_handler.handle(exception)

    @query_debugger
    @action(methods=['GET'], url_path='get', detail=False)
    def get_book(self, request):
        try:
            data = self.request_handler.handle(request)
            uid_book = data.get_para_value('uid')
            if not uid_book:
                raise exceptions.InvalidArgumentException(message=messages.BOOK_NOT_FOUND)
            book = Book.objects.get(uid=uid_book)
            response_data = BookSerializer(book).data
            return self.response_handler.handle(data=response_data)
        except Exception as exception:
            return self.exception_handler.handle(exception)

    @query_debugger
    @action(methods=['POST'], url_path='create', detail=False)
    def create_book(self, request):
        try:
            data = self.request_handler.handle(request)
            create_book_dict = {
                k: data.get_body_value(k, None) for k in self.book_fields if data.get_body_value(k) is not None
            }
            serializer = BookSerializer(data=create_book_dict)
            book = course_utils.create_book_by_dict(create_book_dict = create_book_dict)
            response_data = BookSerializer(book).data
            return self.response_handler.handle(data=response_data)
        except Exception as exception:
            return self.exception_handler.handle(exception)
    @query_debugger
    @action(methods=['POST'], url_path='update', detail=False)
    def update_book(self, request):
        try:
            data = self.request_handler.handle(request)
            uid_book = data.get_body_value('uid')
            book = course_utils.get_book(uid = uid_book)
            update_book_dict = {
                k: data.get_body_value(k, None) for k in self.book_fields if data.get_body_value(k) is not None
            }

            if update_book_dict.get('author'):
                update_book_dict['author'] = course_utils.get_author(update_book_dict.get('author'))
            if update_book_dict.get('categories'):
                update_book_dict['categories'] = course_utils.get_category(update_book_dict.get('categories'))

            book_new = course_utils.update_book_by_dict(book=book, update_book_dict=update_book_dict)
            response_data = BookSerializer(book).data
            return self.response_handler.handle(data=response_data)
        except Exception as exception:
            return self.exception_handler.handle(exception)
    
    @action(methods=['DELETE'], url_path='delete', detail=False)
    def delete(self, request):
        try:
            data = self.request_handler.handle(request)
            uid_book = data.get_body_value('uid')
            book = course_utils.get_book(uid = uid_book)
            book.delete()
            return self.response_handler.handle()
        except Exception as exception:
            return self.exception_handler.handle(exception)

    @action(methods=['GET'], url_path='export_pdf', detail=False)
    def export_pdf(self, request):
        try:
            # buffer = io.BytesIO()

            # # Create the PDF object, using the buffer as its "file."
            # p = canvas.Canvas(buffer, pagesize=A4)

            # # Draw things on the PDF. Here's where the PDF generation happens.
            # # See the ReportLab documentation for the full list of functionality.
            # p.drawString(50, 50, "Hello world.")

            # # Close the PDF object cleanly, and we're done.
            # p.showPage()
            # p.save()

            # # FileResponse sets the Content-Disposition header so that browsers
            # # present the option to save the file.
            # buffer.seek(0)
            # return FileResponse(buffer, as_attachment=True, filename='hello.pdf')
            #---------------------------
            response = HttpResponse(content_type = 'application/pdf')
            d = datetime.today().strftime('%y-%m-%d')
            response['Content-Disposition'] = f'inline; filename = "{d}.pdf"'

            buffer = io.BytesIO()
            p = canvas.Canvas(buffer, pagesize=A4)

            data = {
                [1, 2, 3], 
                [4, 5, 6],
                [7, 8, 9],
            }

            # Start writing pdf here
            p.setFont("Helvetica", 15, leading=None)
            xl = 50
            yl = 800
            # Render data
            # for k,v in data.items():
            #     p.setFont("Helvetica", 15, leading=None)
            #     p.drawString(xl, yl, f"{k}")
            #     # for value in v:
            #     #     for key, val in value.items():
            #     #         p.setFont("Helvetica", 15, leading=None)
            #     #         p.drawString(xl, yl-20, f"{key} - {val}")
            #     xl =  xl + 225
            yl = yl - 90
            for i in range(1,90):
                p.setFont("Helvetica", 15, leading=None)
                p.drawString(xl, yl, f"{i}")
                # for value in v:
                #     for key, val in value.items():
                #         p.setFont("Helvetica", 15, leading=None)
                #         p.drawString(xl, yl-20, f"{key} - {val}")
                xl =  xl + 225
            p.setTitle(f"Report on {d}")
            p.showPage()
            p.save()
            pdf = buffer.getvalue()
            buffer.close()
            response.write(pdf)

            return response
        except Exception as exception:
            return self.exception_handler.handle(exception)
        

        
        
    
        