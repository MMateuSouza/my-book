from django import forms
from django.db.models import fields

from audiobooks.models import Book, BookAuthor, Chapter


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'publishing_company', 'edition', 'isbn_10', 'isbn_13']


class BookAuthorForm(forms.ModelForm):
    class Meta:
        model = BookAuthor
        fields = ['name']


class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['title']
