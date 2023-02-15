from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext as _
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, UserCreateForm
from django.contrib.auth.models import User
from django.contrib import messages


LOGIN_ERROR = 'Пожалуйста, введите правильные имя пользователя и пароль.' \
              ' Оба поля могут быть чувствительны к регистру.'
LOGIN_SUCCESS = 'Вы залогинены'
LOGOUT_SUCCESS = 'Вы разлогинены'
REGISTRATION_SUCCESS = 'Пользователь успешно зарегистрирован'
AUTHENTICATION_ERROR = 'Вы не авторизованы! Пожалуйста, выполните вход.'
USER_UPDATE_SUCCESS = 'Пользователь успешно изменён'
USER_DELETE_SUCCESS = 'Пользователь успешно удалён'
USER_UPDATE_ERROR = 'У вас нет прав для изменения другого пользователя.'


class MainView(View):

    def get(self, request):
        return render(request, 'main.html')


class UsersView(View):

    def get(self, request):
        current_user = None
        if request.user.is_authenticated:
            current_user = request.user
        users = User.objects.all().exclude(is_staff=True)
        return render(request, 'users.html', {'users': users, 'current_user': current_user})


class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user_data = form.cleaned_data
            user = authenticate(
                username = user_data.get('username'),
                password = user_data.get('password')
            )
            if user and user.is_active:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, LOGIN_SUCCESS)
                return redirect('main')

        messages.add_message(request, messages.ERROR, LOGIN_ERROR)
        return render(request, 'login.html', {'form': form})


class LogoutView(View):

    def post(self, request):
        logout(request)
        messages.add_message(request, messages.INFO, LOGOUT_SUCCESS)
        return redirect('main')




class RegistrationView(View):

    def get(self, request):
        form = UserCreateForm()
        return render(request, 'create_user.html', {'form': form})

    def post(self, request):
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, REGISTRATION_SUCCESS)
            return redirect('login')
        return render(request, 'create_user.html', {'form': form})


class UpdateUserView(View):

    def get(self, request, **kwargs):
        pk = kwargs.get('pk')
        user = get_object_or_404(User, id=pk)
        if request.user.is_authenticated:
            if request.user.id != user.id:
                messages.add_message(request, messages.ERROR, USER_UPDATE_ERROR)
                return redirect('users')
            form = UserCreateForm(initial={
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name
            })
            return render(request, 'update_user.html', {'form': form, 'user': user, 'username': user.username})
        messages.add_message(request, messages.ERROR, AUTHENTICATION_ERROR)
        return redirect('login')

    def post(self, request, **kwargs):
        pk = kwargs.get('pk')
        user = get_object_or_404(User, id=pk)
        username = user.username
        if request.user.is_authenticated:
            form = UserCreateForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, USER_UPDATE_SUCCESS)
                return redirect('users')
            return render(request, 'update_user.html', {'form': form, 'user': user, 'username': username})
        messages.add_message(request, messages.ERROR, AUTHENTICATION_ERROR)
        return redirect('login')


class DeleteUserView(View):

    def get(self, request, **kwargs):
        pk = kwargs.get('pk')
        user = get_object_or_404(User, id=pk)
        if request.user.is_authenticated:
            if request.user.id != user.id:
                messages.add_message(request, messages.ERROR, USER_UPDATE_ERROR)
                return redirect('users')
            return render(request, 'delete_user.html', {'user': user})
        messages.add_message(request, messages.ERROR, AUTHENTICATION_ERROR)
        return redirect('login')

    def post(self, request, **kwargs):
        pk = kwargs.get('pk')
        user = get_object_or_404(User, id=pk)
        if request.user.is_authenticated:
            user.delete()
            messages.add_message(request, messages.SUCCESS, USER_DELETE_SUCCESS)
            return redirect('users')
        messages.add_message(request, messages.ERROR, AUTHENTICATION_ERROR)
        return redirect('login')
