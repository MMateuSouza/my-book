from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index(request):
    return render(request, template_name='audiobooks/index.html')


@login_required
def create(request):
    return render(request, template_name='audiobooks/create.html')


@login_required
def recording(request):
    return render(request, template_name='audiobooks/recording.html')
