from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import UserCreateForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.translation import gettext as _


REGISTRATION_SUCCESS = _("User successfully registered")
AUTHENTICATION_ERROR = _("You are not authorized! Please sign in.")
USER_UPDATE_SUCCESS = _("User updated successfully")
USER_DELETE_SUCCESS = _("User deleted successfully")
USER_UPDATE_ERROR = _("You do not have rights to change another user.")


class UsersView(View):
    def get(self, request):
        current_user = None

        if request.user.is_authenticated:
            current_user = request.user

        users = User.objects.all().exclude(is_staff=True)

        return render(
            request,
            "user/users.html",
            {"users": users, "current_user": current_user},
        )


class RegistrationView(View):
    def get(self, request):
        form = UserCreateForm()
        return render(request, "user/create_user.html", {"form": form})

    def post(self, request):
        form = UserCreateForm(request.POST)

        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.SUCCESS, REGISTRATION_SUCCESS
            )

            return redirect("login")

        return render(request, "user/create_user.html", {"form": form})


class UpdateUserView(View):
    def get(self, request, **kwargs):
        pk = kwargs.get("pk")
        user = get_object_or_404(User, id=pk)

        if request.user.is_authenticated:
            if request.user.id != user.id:
                messages.add_message(
                    request, messages.ERROR, USER_UPDATE_ERROR
                )

                return redirect("users")

            form = UserCreateForm(
                initial={
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                }
            )

            return render(
                request,
                "user/update_user.html",
                {"form": form, "user": user, "username": user.username},
            )

        messages.add_message(request, messages.ERROR, AUTHENTICATION_ERROR)
        return redirect("login")

    def post(self, request, **kwargs):
        pk = kwargs.get("pk")
        user = get_object_or_404(User, id=pk)
        username = user.username

        if request.user.is_authenticated:
            if request.user.id != user.id:
                messages.add_message(
                    request, messages.ERROR, USER_UPDATE_ERROR
                )

                return redirect("users")

            form = UserCreateForm(request.POST, instance=user)

            if form.is_valid():
                form.save()
                messages.add_message(
                    request, messages.SUCCESS, USER_UPDATE_SUCCESS
                )

                return redirect("users")

            return render(
                request,
                "user/update_user.html",
                {"form": form, "user": user, "username": username},
            )

        messages.add_message(request, messages.ERROR, AUTHENTICATION_ERROR)
        return redirect("login")


class DeleteUserView(View):
    def get(self, request, **kwargs):
        pk = kwargs.get("pk")
        user = get_object_or_404(User, id=pk)

        if request.user.is_authenticated:
            if request.user.id != user.id:
                messages.add_message(
                    request, messages.ERROR, USER_UPDATE_ERROR
                )

                return redirect("users")

            return render(request, "user/delete_user.html", {"user": user})

        messages.add_message(request, messages.ERROR, AUTHENTICATION_ERROR)
        return redirect("login")

    def post(self, request, **kwargs):
        pk = kwargs.get("pk")
        user = get_object_or_404(User, id=pk)

        if request.user.is_authenticated:
            if request.user.id != user.id:
                messages.add_message(
                    request, messages.ERROR, USER_UPDATE_ERROR
                )

                return redirect("users")

            user.delete()
            messages.add_message(
                request, messages.SUCCESS, USER_DELETE_SUCCESS
            )

            return redirect("users")

        messages.add_message(request, messages.ERROR, AUTHENTICATION_ERROR)
        return redirect("login")
