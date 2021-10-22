from django import forms
from django.db.models import fields

from audiobooks.models import Book, BookAuthor, Chapter


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'publishing_company', 'edition', 'isbn_10', 'isbn_13', 'front_cover']

        error_messages = {
            'title': {
                'required': 'Título é um campo obrigatório'
            },
            'publishing_company': {
                'required': 'Editora é um campo obrigatório'
            },
            'edition': {
                'required': 'Edição é um campo obrigatório'
            },
            'isbn_10': {
                'required': 'ISBN 10 é um campo obrigatório'
            },
            'isbn_13': {
                'required': 'ISBN 13 é um campo obrigatório'
            },
            'front_cover': {
                'required': 'Foto de capa é um campo obrigatório'
            },
        }


class BookAuthorForm(forms.ModelForm):
    class Meta:
        model = BookAuthor
        fields = ['name']


class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['title']
