from django import forms
from django.db.models import fields

from audiobooks.models import Book, BookAuthor, Chapter


class BookForm(forms.ModelForm):
    authors_names = forms.CharField()
    chapters_str = forms.CharField()

    class Meta:
        model = Book
        fields = ['title', 'publishing_company', 'edition',
                  'isbn_10', 'isbn_13', 'front_cover', 'authors_names',
                  'chapters_str',]

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

    def clean_authors_names(self):
        authors_names = self.cleaned_data.get("authors_names")
        authors_names_lst = []

        if authors_names:
            authors_names_lst = authors_names.split(';')

        return authors_names_lst

    def clean_chapters_str(self):
        chapters_str = self.cleaned_data.get('chapters_str')
        return Book.convert_chapters_str_to_json(chapters_str)

    def save(self):
        super().save()

        # Persistência de Autores

        stored_authors_names = self.instance.authors_lst
        authors_names = self.cleaned_data.get('authors_names')
        for author_name in authors_names:
            if author_name not in stored_authors_names:
                BookAuthor(book=self.instance, name=author_name).save()

        deleted_authors = [_ for _ in stored_authors_names if _ not in authors_names]
        for deleted_author in deleted_authors:
            BookAuthor.objects.filter(book=self.instance, name=deleted_author).delete()

        # Persistência de Capítulos

        chapters_dict = self.cleaned_data.get('chapters_str')
        print(chapters_dict)



class BookAuthorForm(forms.ModelForm):
    class Meta:
        model = BookAuthor
        fields = ['name']


class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['title']
