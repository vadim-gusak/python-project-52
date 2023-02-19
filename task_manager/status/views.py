from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Status
from .forms import StatusForm
from django.utils.translation import gettext as _


AUTHENTICATION_ERROR = _("You are not authorized! Please sign in.")
STATUS_CREATE_SUCCESS = _("Status created successfully")
STATUS_UPDATE_SUCCESS = _("Status updated successfully")
STATUS_DELETE_SUCCESS = _("Status deleted successfully")


class StatusesView(View):
    def get(self, request):
        if request.user.is_authenticated:
            statuses = Status.objects.all()
            return render(
                request, "status/statuses.html", {"statuses": statuses}
            )

        messages.add_message(request, messages.ERROR, AUTHENTICATION_ERROR)
        return redirect("login")


class StatusCreateView(View):
    def get(self, request):
        if request.user.is_authenticated:
            form = StatusForm()
            return render(request, "status/create.html", {"form": form})

        messages.add_message(request, messages.ERROR, AUTHENTICATION_ERROR)
        return redirect("login")

    def post(self, request):
        if request.user.is_authenticated:
            form = StatusForm(request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(
                    request, messages.SUCCESS, STATUS_CREATE_SUCCESS
                )
                return redirect("statuses")

        messages.add_message(request, messages.ERROR, AUTHENTICATION_ERROR)
        return redirect("login")


class StatusUpdateView(View):
    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            pk = kwargs.get("pk")
            status = get_object_or_404(Status, id=pk)
            form = StatusForm(initial={"name": status.name})
            return render(
                request, "status/update.html", {"form": form, "status": status}
            )

        messages.add_message(request, messages.ERROR, AUTHENTICATION_ERROR)
        return redirect("login")

    def post(self, request, **kwargs):
        if request.user.is_authenticated:
            pk = kwargs.get("pk")
            status = get_object_or_404(Status, id=pk)
            form = StatusForm(request.POST, instance=status)

            if form.is_valid():
                form.save()
                messages.add_message(
                    request, messages.SUCCESS, STATUS_UPDATE_SUCCESS
                )
                return redirect("statuses")

            return render(
                request, "status/update.html", {"form": form, "status": status}
            )

        messages.add_message(request, messages.ERROR, AUTHENTICATION_ERROR)
        return redirect("login")


class StatusDeleteView(View):
    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request, messages.ERROR, AUTHENTICATION_ERROR)
            return redirect("login")

        pk = kwargs.get("pk")
        status = get_object_or_404(Status, id=pk)
        return render(request, "status/delete.html", {"status": status})

    def post(self, request, **kwargs):
        """
        Добавить проверку задач с данным статусом
        """
        if not request.user.is_authenticated:
            messages.add_message(request, messages.ERROR, AUTHENTICATION_ERROR)
            return redirect("login")

        pk = kwargs.get("pk")
        status = get_object_or_404(Status, id=pk)
        status.delete()
        messages.add_message(request, messages.SUCCESS, STATUS_DELETE_SUCCESS)
        return redirect("statuses")
