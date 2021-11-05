from constance import config
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from audiobooks.forms import AudioBook, AudioBookForm, Book, BookForm
from audiobooks.models import AudioBookChapter


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
    audiobooks = AudioBook.objects.filter(book=book)
    has_audiobooks = audiobooks.count() > 0

    return render(request, context=locals(), template_name='audiobooks/audiobooks.html')


@login_required
def recording(request, book_id, audiobook_id=None):
    book = Book.objects.get(id=book_id)
    audiobook = AudioBook.objects.get(id=audiobook_id) if audiobook_id else AudioBook()

    if request.method == 'GET':
        form = AudioBookForm(instance=audiobook)
    elif request.method == 'POST':
        form = AudioBookForm(request.POST, instance=audiobook)

        if form.is_valid():
            created_or_updated_msg = 'modificada' if audiobook.id else 'registrada'
            form.save()
            AudioBook.persist_audiobook_chapters(audiobook=form.instance, files=request.FILES)
            messages.success(request, f'Gravação {created_or_updated_msg} com sucesso!')
            return redirect('audiobooks:audiobooks', id=book.id)

    return render(request, context=locals(), template_name='audiobooks/recording.html')
