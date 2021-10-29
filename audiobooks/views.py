from constance import config
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from audiobooks.forms import BookForm
from audiobooks.models import Book


@login_required
def index(request):
    books_list = Book.objects.all().order_by('id')
    paginator = Paginator(books_list, config.ELEMENTS_PER_PAGE)
    has_books = paginator.count != 0
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, context={'page_obj': page_obj, 'has_books': has_books}, template_name='audiobooks/index.html')


@login_required
def create(request, id=None):
    book = Book.objects.get(id=id) if id else Book()

    if request.method == 'GET':
        form = BookForm(instance=book)
    elif request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)

        if form.is_valid():
            created_or_updated_msg = 'modificado' if book.id else 'criado'
            form.save()
            messages.success(request, f'Livro {created_or_updated_msg} com sucesso!')
            return redirect('audiobooks:index')

    return render(request, context=locals(), template_name='audiobooks/create.html')


@login_required
def audiobooks(request, id):
    book = Book.objects.get(id=id)

    return render(request, context={'book': book}, template_name='audiobooks/audiobooks.html')


@login_required
def recording(request, id):
    # TODO: Implementar persistência de audios para um livro.
    return render(request, template_name='audiobooks/recording.html')
