from django.urls import path
from .views import RegistrationView
from .views import UpdateUserView, DeleteUserView, UsersView

urlpatterns = [
    path("", UsersView.as_view(), name="users"),
    path("create/", RegistrationView.as_view(), name="create_user"),
    path("<int:pk>/update/", UpdateUserView.as_view(), name="update_user"),
    path("<int:pk>/delete/", DeleteUserView.as_view(), name="delete_user"),
]
