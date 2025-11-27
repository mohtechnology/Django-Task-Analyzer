from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("add_task/", views.add_tasks),
    path("edit/<int:task_id>/", views.edit_task, name="edit_task"),
    path("delete/<int:task_id>/", views.delete_task, name="delete_task"),
]