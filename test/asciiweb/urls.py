from django.urls import path
from . import views

app_name = "asciiweb"

urlpatterns = [
        path("", views.home, name="home"),
        ]
