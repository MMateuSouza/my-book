from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator
from django.shortcuts import render


def index(request):
    users_list = User.objects.all().order_by('id')
    paginator = Paginator(users_list, 10)  # TODO: Modificar esta quantidade para algo dinâmico (Django Constance)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, context={'page_obj': page_obj}, template_name='users/index.html')


def create(request, id=None):
    user = User.objects.get(id=id) if id else User()

    if request.method == 'POST':
        # TODO: Adicionar cadastro/edição de usuário
        pass
        return

    groups = Group.objects.all()
    return render(request, context=locals(), template_name='users/create.html')
