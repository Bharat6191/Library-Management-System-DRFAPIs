from django.db import models
# from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_librarian = models.BooleanField(default=False)

    def __str__(self):
        return self.email


class Book(models.Model):
    title = models.CharField(max_length=255)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class BorrowRequest(models.Model):
    user = models.ForeignKey(User, related_name='borrow_requests', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='borrow_requests', on_delete=models.CASCADE)
    date_start = models.DateField()
    date_end = models.DateField()
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} borrowing {self.book.title}"
