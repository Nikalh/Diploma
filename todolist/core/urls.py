from django.urls import path, include

from todolist.core.views import SingUpView, LoginView, ProfileView, UpdatePasswordView

urlpatterns = [
    path('sign-up', SingUpView.as_view(), name='sign-up'),
    path('login', LoginView.as_view(), name='login'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('update_password', UpdatePasswordView.as_view(), name='update_password'),


]
