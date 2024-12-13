import csv
from django.http import HttpResponse
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from .models import User, Book, BorrowRequest
from .serializers import UserSerializer, BookSerializer, BorrowRequestSerializer

class LibrarianViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def create_user(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=201)
        return Response(serializer.errors, status=400)

    def list_borrow_requests(self, request):
        borrow_requests = BorrowRequest.objects.filter(approved=False)
        serializer = BorrowRequestSerializer(borrow_requests, many=True)
        return Response(serializer.data)

    def update_borrow_request(self, request, pk=None):
        borrow_request = BorrowRequest.objects.get(pk=pk)
        action = request.data.get('action')
        if action == 'approve':
            borrow_request.approved = True
        elif action == 'deny':
            borrow_request.delete()
        borrow_request.save()
        return Response({"message": f"Request {action}d successfully"}, status=200)

    def user_borrow_history(self, request, user_id=None):
        user = User.objects.get(pk=user_id)
        borrow_history = BorrowRequest.objects.filter(user=user)
        serializer = BorrowRequestSerializer(borrow_history, many=True)
        return Response(serializer.data)

class UserViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list_books(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def borrow_book(self, request):
        user = request.user
        book_id = request.data.get('book_id')
        date_start = request.data.get('date_start')
        date_end = request.data.get('date_end')

        book = Book.objects.get(pk=book_id)
        if BorrowRequest.objects.filter(book=book, date_start__lte=date_end, date_end__gte=date_start).exists():
            return Response({"message": "Book is already borrowed during this period"}, status=400)

        borrow_request = BorrowRequest.objects.create(
            user=user,
            book=book,
            date_start=date_start,
            date_end=date_end
        )
        borrow_request.save()
        return Response({"message": "Borrow request submitted successfully"}, status=201)

    def borrow_history(self, request):
        user = request.user
        borrow_history = BorrowRequest.objects.filter(user=user)
        serializer = BorrowRequestSerializer(borrow_history, many=True)
        return Response(serializer.data)

    def download_borrow_history(self, request):
        user = request.user
        borrow_history = BorrowRequest.objects.filter(user=user)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="borrow_history.csv"'
        writer = csv.writer(response)
        writer.writerow(['Book Title', 'Date Start', 'Date End'])
        for history in borrow_history:
            writer.writerow([history.book.title, history.date_start, history.date_end])
        return response