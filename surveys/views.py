from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Profile


def index(request):
    return render(request, 'surveys/index.html')


def profile(request):
    return render(request, 'surveys/profile.html')


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        gender = request.POST.get("gender")
        country = request.POST.get("country")
        age = request.POST.get("age")

        if password1 != password2:
            return render(request, "surveys/register.html", {"error": "Пароли не совпадают"})

        if User.objects.filter(username=username).exists():
            return render(request, "surveys/register.html", {"error": "Такой логин уже существует"})

        user = User.objects.create_user(username=username, password=password1)

        Profile.objects.create(
            user=user,
            gender=gender,
            country=country,
            age=age
        )

        return redirect("/")

    return render(request, "surveys/register.html")
