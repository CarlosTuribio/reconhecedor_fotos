from textwrap import indent

from django.urls import path
from .views import index

app_name = 'reconhecedor'

urlpatterns = [
    path('', index)
]

