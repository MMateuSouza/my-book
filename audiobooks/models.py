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

    def __str__(self):
        return self.title

    @property
    def authors_lst(self):
        authors = BookAuthor.objects.filter(book=self)
        return [author.name for author in authors]

    @property
    def authors(self):
        return ', '.join(self.authors_lst)

    @property
    def main_chapters(self):
        return Chapter.objects.filter(book=self, main=True).order_by('sequence')

    @property
    def chapters_quantity(self):
        # Contabiliza apenas capítulos principais/raíz
        return self.main_chapters.count()

    @property
    def chapters_str(self):
        return Book.convert_chapters_obj_to_json(self.main_chapters)

    @staticmethod
    def convert_chapters_obj_to_json(chapters_obj):
        chapters_json = []

        for chapter_obj in chapters_obj:
            chapter_dict = dict()
            chapter_dict.update({ 'id': chapter_obj.id })
            chapter_dict.update({ 'title': chapter_obj.title })
            subchapters = Book.convert_chapters_obj_to_json(chapter_obj.subchapters.all().order_by('sequence'))
            chapter_dict.update({ 'subchapters': subchapters })

            chapters_json.append(chapter_dict)

        return chapters_json

    @property
    def ordered_chapters_list(self):
        return Book.get_ordered_chapters_list(self.main_chapters)

    @staticmethod
    def get_ordered_chapters_list(chapters_obj):
        chapters_lst = []

        for chapter_obj in chapters_obj:
            chapters_lst.append(chapter_obj)
            chapters_lst += Book.get_ordered_chapters_list(chapter_obj.subchapters.all().order_by('sequence'))

        return chapters_lst

    @staticmethod
    def convert_chapters_str_to_json(chapters_str):
        if not chapters_str:
            return

        return json.loads(chapters_str)

    @staticmethod
    def persist_chapters(book, chapters=[], main=True):
        chapters_instances = []

        for chapter in chapters:
            subchapters = chapter['subchapters'] if 'subchapters' in chapter else []
            subchapters_instances = []

            if subchapters:
                subchapters_instances = Book.persist_chapters(book, subchapters, False)

            title = chapter['title'] if 'title' in chapter else ''
            sequence = chapter['sequence'] if 'sequence' in chapter else 0
            chapter_instance = Chapter(book=book, title=title, main=main, sequence=sequence)
            chapter_instance.save()

            for subchapter_instance in subchapters_instances:
                chapter_instance.subchapters.add(subchapter_instance)

            chapters_instances.append(chapter_instance)
        return chapters_instances


class BookAuthor(models.Model):
    book = models.ForeignKey(verbose_name='Livro', to='audiobooks.Book', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Autor', max_length=255)

    def __str__(self):
        return self.name


class Chapter(models.Model):
    book = models.ForeignKey(verbose_name='Livro', to='audiobooks.Book', null=True, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Título', max_length=255)
    main = models.BooleanField(verbose_name='Principal')
    sequence = models.PositiveSmallIntegerField(verbose_name='Sequência', null=True)
    subchapters = models.ManyToManyField(verbose_name='Subcapítulos', to='self', blank=True, symmetrical=False)

    def __str__(self):
        return self.title
