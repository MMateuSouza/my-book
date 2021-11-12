from constance import config
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from users.forms import User, UserForm


@login_required
@permission_required('users.view_user')
def index(request):
    users_list = User.objects.all().order_by('id')
    paginator = Paginator(users_list, config.ELEMENTS_PER_PAGE)
    has_users = paginator.count != 0
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, context={'page_obj': page_obj, 'has_users': has_users}, template_name='users/index.html')


@login_required
@permission_required('users.add_user')
@permission_required('users.change_user')
def create(request, id=None):
    user = User.objects.get(id=id) if id else User()

    if request.method == 'GET':
        form = UserForm(instance=user)
    elif request.method == 'POST':
        form = UserForm(request.POST, instance=user)

        if form.is_valid():
            created_or_updated_msg = 'modificado' if user.id else 'criado'
            form.save()
            messages.success(request, f'Usuário {created_or_updated_msg} com sucesso!')
            return redirect('users:index')

    groups = Group.objects.all()
    return render(request, context=locals(), template_name='users/create.html')


@login_required
@permission_required('users.delete_user')
def delete(request, id):
    user = User.objects.get(id=id).delete()
    messages.success(request, f'Usuário excluído com sucesso!')
    return redirect('users:index')
