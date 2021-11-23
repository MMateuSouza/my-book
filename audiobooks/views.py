from constance import config
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

import json

from audiobooks.forms import AudioBook, AudioBookChapter, AudioBookForm, Book, BookForm, Favorite
from users.models import User


@login_required
@permission_required('audiobooks.view_book')
def index(request):
    q = request.GET.get('q', None)

    books_list = Book.objects.all().order_by('id')
    if q:
        books_list = books_list \
            .filter(
                Q(title__icontains=q) |
                Q(publishing_company__icontains=q) |
                Q(edition__icontains=q) |
                Q(year__icontains=q) |
                Q(isbn_10__icontains=q) |
                Q(isbn_13__icontains=q)
            )
    paginator = Paginator(books_list, config.ELEMENTS_PER_PAGE)
    has_books = paginator.count != 0
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, context={'page_obj': page_obj, 'has_books': has_books, 'q': q}, template_name='audiobooks/index.html')


@login_required
@permission_required('audiobooks.add_book')
@permission_required('audiobooks.change_book')
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
@permission_required('audiobooks.delete_book')
def delete(request, id):
    Book.objects.get(id=id).delete()
    messages.success(request, f'Livro excluído com sucesso!')
    return redirect('audiobooks:index')


@login_required
@permission_required('audiobooks.delete_audiobook')
def delete_audiobook(request, audiobook_id):
    audiobook = AudioBook.objects.get(id=audiobook_id)
    book_id = audiobook.book.id
    audiobook.delete()
    messages.success(request, f'Audiobook excluído com sucesso!')
    return redirect('audiobooks:audiobooks', id=book_id)


@login_required
@permission_required('audiobooks.view_audiobook')
def audiobooks(request, id):
    book = Book.objects.get(id=id)
    audiobooks = AudioBook.objects.filter(book=book)
    has_audiobooks = audiobooks.count() > 0

    return render(request, context=locals(), template_name='audiobooks/audiobooks.html')


@login_required
@permission_required('audiobooks.add_audiobook')
@permission_required('audiobooks.change_audiobook')
def recording(request, book_id, audiobook_id=None):
    book = Book.objects.get(id=book_id)
    storytellers = User.objects.filter(groups__name='Narrador').order_by('id')
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


@login_required
@permission_required('audiobooks.view_audiobook')
def play(request, audiobook_id, chapter_id=None):
    audiobook = AudioBook.objects.get(id=audiobook_id)

    if chapter_id:
        audiobook_chapter = AudioBookChapter.objects.filter(audiobook=audiobook, chapter__id=chapter_id).first()
        return JsonResponse({'recording_file': audiobook_chapter.get_recording_file}, safe=False)

    return render(request, context=locals(), template_name='audiobooks/play.html')


@login_required
@csrf_exempt
def favorite(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id, audiobook_id = data['userId'] if 'userId' in data else None, data['audioBookId'] if 'audioBookId' in data else None
        success, removed, message = Favorite.add_audiobook_to_user_favorites(user_id, audiobook_id)
        return JsonResponse({'success': success, 'removed': removed, 'message': message})
