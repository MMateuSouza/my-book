from django import forms

from audiobooks.models import AudioBook, AudioBookChapter, Book, BookAuthor, Chapter, Favorite


class BookForm(forms.ModelForm):
    authors_names = forms.CharField()
    chapters_str = forms.CharField()

    class Meta:
        model = Book
        fields = ['title', 'publishing_company', 'edition',
                  'isbn_10', 'isbn_13', 'front_cover', 'authors_names',
                  'chapters_str', 'year']

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
            'year': {
                'required': 'Ano é um campo obrigatório'
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
        _, inserted_or_updated_ids = Book.persist_chapters(self.instance, chapters_dict)

        # Remoção dos Capítulos
        Chapter.objects \
            .filter(book=self.instance) \
            .exclude(id__in=inserted_or_updated_ids) \
            .delete()


class AudioBookForm(forms.ModelForm):
    class Meta:
        model = AudioBook
        fields = '__all__'
