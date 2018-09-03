from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from datetime import date

from locallibrary.settings import MEDIA_URL


class Genre(models.Model):
    name = models.CharField(max_length=200, help_text="Введите жанр книги..")

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text="Введите краткое описание книги...")
    isbn = models.CharField('ISBN', max_length=13, help_text="13 символов <a href='https://www.isbn-international.org/content/what-isbn'>ISBN номер</a>")
    genre = models.ManyToManyField('Genre', help_text="Выберите жанр книги..")
    img = models.ImageField(upload_to= 'images/', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def get_short_title(self):
        if self.title.__len__()>30:
            return self.title[:30] + "..."
        else:
            return self.title

    def get_short_summary(self):

        if self.summary.__len__()>120:
            return self.summary[:120] + "..."
        else:
            return self.summary

    def display_genre(self):
        """
        Creates a string for the Genre. This is required to display genre in Admin.
        """
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'

class Language(models.Model):
    name = models.CharField("Название", max_length=200, help_text='Введите язык, на котором пишут книги..')

    def __str__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):

        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):

        return '%s, %s' % (self.last_name, self.first_name)

class BookInstance(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный ID для этой конкретной книги")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    language = models.ForeignKey("Language", on_delete=models.SET_NULL, null=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Обрабатывается'),
        ('o', 'На руках'),
        ('a', 'Доступна'),
        ('r', 'Зарезирвирована'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='d', help_text='Доступность книги')

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Может вернуть книгу"),)

    def __str__(self):

        return '%s (%s)' % (self.id,self.book.title)

    @property
    def is_overdue(self):
        if self.due_back and date.today()> self.due_back:
            return  True
        return False
