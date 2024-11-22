from django.urls import path
from .views import userRegisterView


urlpatterns = [
    path('register/', userRegisterView.as_view())

]
