from django.shortcuts import render


# Pages
def index(request):
    return render(request, 'pages/index.html')

def privacy_policy(request):
    return render(request, 'pages/privacy&policy.html')

def faq(request):
    return render(request, 'pages/faq.html')

def terms(request):
    return render(request, 'pages/terms.html')

def about_us(request):
    return render(request, 'pages/about.html')


def permission_denied(request, *args, **argv):
    response = render(request, 'pages/403.html')
    response.status_code = 403
    return response


def page_not_found(request, *args, **argv):
    response = render(request,'pages/404.html')
    response.status_code = 404
    return response


def server_error(request, *args, **argv):
    response = render(request, 'pages/500.html')
    response.status_code = 500
    return response