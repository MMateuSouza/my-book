from django.core.files import storage
from django.db import models

import json

from project.storage import OverwriteStorage


def directory_path(instance, filename, path):
    extension = filename.split('.')[-1]
    return f'{path}/{instance.id}.{extension}'


def front_cover_directory_path(instance, filename):
    return directory_path(instance, filename, 'front_convers')


def recording_file_directory_path(instance, filename):
    return directory_path(instance, filename, 'audiobooks')


class AudioBook(models.Model):
    MALE = 'M'
    FEMALE = 'F'

    TYPES_OF_VOICES = [
        (MALE, 'Masculina'),
        (FEMALE, 'Feminina'),
    ]

    book = models.ForeignKey(verbose_name='Livro', to='audiobooks.Book', on_delete=models.CASCADE)
    storyteller = models.ForeignKey(verbose_name='Narrador', to='users.User', on_delete=models.CASCADE)
    narration_type = models.CharField(verbose_name='Tipo de Narração', max_length=1, choices=TYPES_OF_VOICES)

    @staticmethod
    def persist_audiobook_chapter(audiobook, description, file):
        _, chapter_id = description.split('_')
        chapter = Chapter.objects.get(id=chapter_id)

        audiobook_chapter = None
        try:
            audiobook_chapter = AudioBookChapter.objects.get(audiobook=audiobook, chapter=chapter)
        except AudioBookChapter.DoesNotExist:
            audiobook_chapter = AudioBookChapter(audiobook=audiobook, chapter=chapter)
            audiobook_chapter.save()

        extension = str(file).split('.')[-1]
        audiobook_chapter.recording_file.save(f'tmp.{extension}', file)

    @staticmethod
    def persist_audiobook_chapters(audiobook, files):
        for file in files:
            AudioBook.persist_audiobook_chapter(audiobook, file, files.get(file))


class AudioBookChapter(models.Model):
    audiobook = models.ForeignKey(verbose_name='Audiobook', to='audiobooks.AudioBook', on_delete=models.CASCADE)
    chapter = models.ForeignKey(verbose_name='Capítulo', to='audiobooks.Chapter', on_delete=models.CASCADE)
    recording_file = models.FileField(verbose_name='Gravação', max_length=255, storage=OverwriteStorage(), upload_to=recording_file_directory_path)

    def save(self, *args, **kwargs):
        if self.pk is None:
            recording_file = self.recording_file
            self.recording_file = None
            super(AudioBookChapter, self).save(*args, **kwargs)
            self.recording_file = recording_file
        super(AudioBookChapter, self).save(*args, **kwargs)


class Book(models.Model):
    title = models.CharField(verbose_name='Título', max_length=255)
    publishing_company = models.CharField(verbose_name='Editora', max_length=64)
    edition = models.PositiveIntegerField(verbose_name='Edição')
    isbn_10 = models.CharField(verbose_name='ISBN 10', max_length=10)
    isbn_13 = models.CharField(verbose_name='ISBN 13', max_length=13)
    front_cover = models.ImageField(verbose_name='Foto de Capa', max_length=255, storage=OverwriteStorage(), upload_to=front_cover_directory_path)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.pk is None:
            front_cover = self.front_cover
            self.front_cover = None
            super(Book, self).save(*args, **kwargs)
            self.front_cover = front_cover
        super(Book, self).save(*args, **kwargs)

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
