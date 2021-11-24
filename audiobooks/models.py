from django.conf import settings
from django.core.files import storage
from django.db import IntegrityError, models
from pydub import AudioSegment

import json
import os
import tempfile

from project.storage import OverwriteStorage
from users.models import User


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

    @property
    def total_pages(self):
        return AudioBookChapter.objects.filter(audiobook=self).last().end_page

    @property
    def chapters(self):
        chapters = []

        for chapter in self.book.ordered_chapters_list:
            audiobook_chapter = AudioBookChapter.objects.filter(audiobook=self, chapter=chapter).first()
            chapters.append(audiobook_chapter)

        return chapters

    @staticmethod
    def get_audiobook_by_id(id):
        try:
            return AudioBook.objects.get(id=id)
        except AudioBook.DoesNotExist:
            return None

    @staticmethod
    def persist_audiobook_chapter(audiobook, description, file, start_page, pages_quantity):
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
        audiobook_chapter.start_page = start_page
        audiobook_chapter.pages_quantity = pages_quantity
        audiobook_chapter.save()

    @staticmethod
    def convert_multiple_files_into_once(filename, files_lst):
        audio_file = None
        format = None

        for i, file in enumerate(files_lst):
            if i == 0:
                audio_file = AudioSegment.from_file(file)
                format = str(file).split('.')[-1]
                # Forçar o formato a ser mp4 quando o arquivo for extensão m4a
                if format == 'm4a':
                    format = 'mp4'
                continue

            audio_file_aux = AudioSegment.from_file(file)
            audio_file += audio_file_aux

        output_dir = os.path.join(tempfile.gettempdir(), f'{filename}.{format}')
        audio_file.export(output_dir, format=format)

        return open(output_dir, 'rb')

    @staticmethod
    def persist_audiobook_chapters(audiobook, files):
        total_pages = 1
        for file in files:
            audio_file = None
            files_lst = files.getlist(file)
            files_lst_length = len(files_lst)

            if files_lst_length > 1:
                audio_file = AudioBook.convert_multiple_files_into_once(file, files_lst)
            elif files_lst_length == 1:
                audio_file = files_lst[0]

            AudioBook.persist_audiobook_chapter(audiobook, file, audio_file, total_pages, files_lst_length)
            total_pages += files_lst_length


class AudioBookChapter(models.Model):
    audiobook = models.ForeignKey(verbose_name='Audiobook', to='audiobooks.AudioBook', on_delete=models.CASCADE)
    chapter = models.ForeignKey(verbose_name='Capítulo', to='audiobooks.Chapter', on_delete=models.CASCADE)
    recording_file = models.FileField(verbose_name='Gravação', max_length=255, storage=OverwriteStorage(), upload_to=recording_file_directory_path)
    start_page = models.IntegerField(verbose_name='Página Inicial do Capítulo', default=0)
    pages_quantity = models.IntegerField(verbose_name='Qtd. Páginas do Capítulo', default=0)

    @property
    def initial_page(self):
        if self.start_page:
            return self.start_page
        return None

    @property
    def end_page(self):
        if self.initial_page:
            return (self.initial_page + self.pages_quantity) - 1
        return None

    def save(self, *args, **kwargs):
        if self.pk is None:
            recording_file = self.recording_file
            self.recording_file = None
            super(AudioBookChapter, self).save(*args, **kwargs)
            self.recording_file = recording_file
        super(AudioBookChapter, self).save(*args, **kwargs)

    @property
    def get_recording_file(self):
        return f'{settings.MEDIA_URL}{self.recording_file}'


class Book(models.Model):
    title = models.CharField(verbose_name='Título', max_length=255)
    publishing_company = models.CharField(verbose_name='Editora', max_length=64)
    edition = models.PositiveIntegerField(verbose_name='Edição')
    year = models.IntegerField(verbose_name='Ano')
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
    def has_chapters(self):
        return self.chapters_quantity != 0

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
        inserted_or_updated_ids = []

        for chapter in chapters:
            subchapters = chapter['subchapters'] if 'subchapters' in chapter else []
            subchapters_instances = []

            if subchapters:
                subchapters_instances, _ = Book.persist_chapters(book, subchapters, False)
                inserted_or_updated_ids += _

            chapter_instance = None
            try:
                id = chapter['id'] if 'id' in chapter and chapter['id'] else None
                chapter_instance = Chapter.objects.get(id=id)
            except Chapter.DoesNotExist:
                chapter_instance = Chapter()

            title = chapter['title'] if 'title' in chapter else ''
            sequence = chapter['sequence'] if 'sequence' in chapter else 0
            chapter_instance.book = book
            chapter_instance.title = title
            chapter_instance.main = main
            chapter_instance.sequence = sequence
            chapter_instance.save()
            inserted_or_updated_ids.append(chapter_instance.id)

            for subchapter_instance in subchapters_instances:
                chapter_instance.subchapters.add(subchapter_instance)

            chapters_instances.append(chapter_instance)
        return chapters_instances, inserted_or_updated_ids


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


class Favorite(models.Model):
    user = models.ForeignKey(verbose_name='Usuário', to='users.User', related_name='favorites', on_delete=models.CASCADE)
    audiobook = models.ForeignKey(verbose_name='Audiobook', to='audiobooks.AudioBook', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'audiobook']

    @staticmethod
    def add_audiobook_to_user_favorites(user_id, audiobook_id):
        user, audiobook = User.get_user_by_id(user_id), AudioBook.get_audiobook_by_id(audiobook_id)
        removed = False

        if not user or not audiobook:
            return False, 'Usuário e/ou AudioBook não encontrado(s)'

        message = ''
        try:
            Favorite(user=user, audiobook=audiobook).save()
            message = 'AudioBook adicionado aos favoritos'
        except IntegrityError:
            Favorite.objects.get(user=user, audiobook=audiobook).delete()
            removed = True
            message = 'AudioBook desfavoritado com sucesso'

        return True, removed, message
