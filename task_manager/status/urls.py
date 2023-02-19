from django.urls import path
from .views import (
    StatusesView,
    StatusCreateView,
    StatusUpdateView,
    StatusDeleteView,
)

urlpatterns = [
    path("", StatusesView.as_view(), name="statuses"),
    path("create/", StatusCreateView.as_view(), name="create_status"),
    path("<int:pk>/update/", StatusUpdateView.as_view(), name="update_status"),
    path("<int:pk>/delete/", StatusDeleteView.as_view(), name="delete_status"),
]
