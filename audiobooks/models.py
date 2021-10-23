from django.db import models

import json

# TODO: Verificar quais campos serão adicionados para instância AudioBook
# class AudioBook(models.Model):
#     pass


class Book(models.Model):
    title = models.CharField(verbose_name='Título', max_length=255)
    publishing_company = models.CharField(verbose_name='Editora', max_length=64)
    edition = models.PositiveIntegerField(verbose_name='Edição')
    isbn_10 = models.CharField(verbose_name='ISBN 10', max_length=10)
    isbn_13 = models.CharField(verbose_name='ISBN 13', max_length=13)
    front_cover = models.ImageField(verbose_name='Foto de Capa', upload_to='front_cover')

    @property
    def authors_lst(self):
        authors = BookAuthor.objects.filter(book=self)
        return [author.name for author in authors]

    @property
    def authors(self):
        return ', '.join(self.authors_lst)

    @property
    def chapters_quantity(self):
        pass

    @staticmethod
    def convert_chapters_str_to_json(chapters_str):
        if not chapters_str:
            return

        return json.loads(chapters_str)

    @staticmethod
    def persist_chapters(chapters=[]):
        chapters_instances = subchapters_instances = []

        for chapter in chapters:
            subchapters = chapter['subchapters'] if 'subchapters' in chapter else []
            if subchapters:
                subchapters_instances, _ = Book.persist_chapters(subchapters)
                chapters_instances += _

            # `chapter_desc` simula a instância de um capítulo
            chapter_desc = chapter['title'] if 'title' in chapter else ''
            # Após criar uma instância será preciso adicionar todas as `subinstâncias` do capítulo à ele
            chapters_instances.append(chapter_desc)
        return subchapters_instances, chapters_instances


class BookAuthor(models.Model):
    book = models.ForeignKey(verbose_name='Livro', to='audiobooks.Book', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Autor', max_length=255)


class Chapter(models.Model):
    book = models.ForeignKey(verbose_name='Livro', to='audiobooks.Book', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Título', max_length=255)
    subchapters = models.ManyToManyField(verbose_name='Subcapítulos', to='self', blank=True)
