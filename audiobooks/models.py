from django import forms
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
    def persist_chapters(chapters=[], main=True):
        chapters_instances = subchapters_instances = []

        for chapter in chapters:
            subchapters = chapter['subchapters'] if 'subchapters' in chapter else []
            if subchapters:
                subchapters_instances, _ = Book.persist_chapters(subchapters, False)
                chapters_instances += _

            title = chapter['title'] if 'title' in chapter else ''
            chapter_instance = Chapter(title=title, main=main)
            chapter_instance.save()
            for subchapter_instance in subchapters_instances:
                chapter_instance.subchapters.add(subchapter_instance)

            chapters_instances.append(chapter_instance)
        return subchapters_instances, chapters_instances


class BookAuthor(models.Model):
    book = models.ForeignKey(verbose_name='Livro', to='audiobooks.Book', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Autor', max_length=255)

    def __str__(self):
        return self.name


class Chapter(models.Model):
    book = models.ForeignKey(verbose_name='Livro', to='audiobooks.Book', null=True, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Título', max_length=255)
    main = models.BooleanField(verbose_name='Principal')
    subchapters = models.ManyToManyField(verbose_name='Subcapítulos', to='self', blank=True)

    def __str__(self):
        return self.title
