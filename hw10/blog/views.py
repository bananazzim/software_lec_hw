from django.shortcuts import render

# Create your views here.


def main_page(request):
    return render(request, 'single_pages/index.html')

def strawberry_page(request):
    return render(request, 'single_pages/strawberry.html')

def about_page(request):
    return render(request, 'single_pages/about.html')