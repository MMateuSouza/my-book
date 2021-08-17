from constance import config
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator
from django.shortcuts import render

from users.forms import UserForm


def index(request):
    users_list = User.objects.all().order_by('id')
    paginator = Paginator(users_list, config.ELEMENTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, context={'page_obj': page_obj}, template_name='users/index.html')


def create(request, id=None):
    user = User.objects.get(id=id) if id else User()

    if request.method == 'GET':
        form = UserForm(instance=user)
    elif request.method == 'POST':
        form = UserForm(request.POST, instance=user)

        if form.is_valid():
            print()
        else:
            print(form.errors)

    groups = Group.objects.all()
    return render(request, context=locals(), template_name='users/create.html')
