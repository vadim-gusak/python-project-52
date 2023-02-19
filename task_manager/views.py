from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm


LOGIN_SUCCESS = "Вы залогинены"
LOGOUT_SUCCESS = "Вы разлогинены"
LOGIN_ERROR = (
    "Пожалуйста, введите правильные имя пользователя и пароль. "
    "Оба поля могут быть чувствительны к регистру."
)


class MainView(View):
    def get(self, request):
        return render(request, "main.html")


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            user_data = form.cleaned_data
            user = authenticate(
                username=user_data.get("username"),
                password=user_data.get("password"),
            )

            if user and user.is_active:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, LOGIN_SUCCESS)

                return redirect("main")

        messages.add_message(request, messages.ERROR, LOGIN_ERROR)

        return render(request, "login.html", {"form": form})


class LogoutView(View):
    def post(self, request):
        logout(request)
        messages.add_message(request, messages.INFO, LOGOUT_SUCCESS)

        return redirect("main")
