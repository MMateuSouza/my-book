from django.shortcuts import render


def index(request):
    return render(request, template_name='main/index.html')


def sign_in(request):
    return render(request, template_name='main/index.html')


def sign_out(request):
    return render(request, template_name='main/index.html')
