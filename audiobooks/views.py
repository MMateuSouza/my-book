from django.shortcuts import render


def index(request):
    return render(request, template_name='audiobooks/index.html')


def create(request):
    return render(request, template_name='audiobooks/create.html')


def recording(request):
    return render(request, template_name='audiobooks/recording.html')
