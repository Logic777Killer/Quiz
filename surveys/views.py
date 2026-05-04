from django.shortcuts import render

def index(request):
    return render(request, 'surveys/index.html')

def profile(request):
    return render(request, 'surveys/profile.html')

