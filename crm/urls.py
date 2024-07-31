from django.urls import path
from . import views

urlpatterns = [
    path('static-page/', views.static_admin, name='static_admin'),
]

