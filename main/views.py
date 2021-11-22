from constance import config
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from audiobooks.forms import AudioBook
from users.forms import Group, User, UserForm


@login_required
@permission_required('audiobooks.view_audiobook')
def index(request):
    q = request.GET.get('q', None)

    audiobooks_lst = AudioBook.objects.all().order_by('id')
    if q:
        audiobooks_lst = audiobooks_lst.filter(book__title__icontains=q)
    paginator = Paginator(audiobooks_lst, config.ELEMENTS_PER_PAGE)
    has_audiobooks = paginator.count != 0
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, context=locals(), template_name='main/index.html')


def sign_in(request):
    if request.user.is_authenticated:
        return redirect('main:index')

    elif request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        remember_me = True if request.POST.get('remember_me', None) == 'on' else False

        user = authenticate(request, username=username, password=password)
        if user:
            request.session.set_expiry(config.TIME_TO_EXPIRE_SESSION) if remember_me else request.session.set_expiry(0)
            login(request, user)
            return redirect('main:index')
        messages.error(request, 'Usuário ou senha incorretos.')

    return render(request, template_name='main/sign_in.html')


def sign_out(request):
    logout(request)
    messages.success(request, 'Sessão encerrada com sucesso.')
    return redirect('main:sign_in')


def sign_up(request):
    user = User()
    group = Group.objects.filter(name='Ouvinte').first()

    if request.method == 'GET':
        form = UserForm(instance=user)
    elif request.method == 'POST':
        form = UserForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário criado com sucesso!')
            return redirect('main:sign_in')

    return render(request, context=locals(), template_name='main/sign_up.html')