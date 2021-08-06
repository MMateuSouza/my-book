from django.shortcuts import redirect, render


def index(request):
    return render(request, template_name='main/index.html')


def sign_in(request):
    if request.method == 'POST':
        return redirect('main:index')
    return render(request, template_name='main/sign_in.html')


def sign_out(request):
    return redirect('main:sign_in')
