from django.shortcuts import render
from django.utils.translation import gettext as _


def hello_view(request):
    text = _('Hello, worlddd!')
    return render(request, 'base.html', {'text': text})
