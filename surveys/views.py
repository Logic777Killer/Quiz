from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Profile


def index(request):
    return render(request, 'surveys/index.html')


@login_required
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


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is None:
            return render(request, "surveys/login.html", {"error": "Неверный логин или пароль"})

        login(request, user)
        return redirect("/")

    return render(request, "surveys/login.html")


def logout_view(request):
    logout(request)
    return redirect("/")

