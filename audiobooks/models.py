from django.db import models


class Chapter(models.Model):
    pass


# TODO: Verificar quais campos serão adicionados para instância Livro
class Book(models.Model):
    title = None
    publishing_company = None
    authors = None
    edition = None
    isbn_10 = None
    isbn_13 = None
    chapters = None


# TODO: Verificar quais campos serão adicionados para instância AudioBook
class AudioBook(models.Model):
    pass
