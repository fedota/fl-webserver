from . import views
from django.urls import path

app_name = "fedota"
urlpatterns = [
    path("<int:id>/start/", views.start_problem, name="start_problem"),
    path("<int:id>/stop/", views.stop_problem, name="stop_problem"),
]