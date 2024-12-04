from django.urls import path
from .views import OneFormsView, ResultsView, index

urlpatterns = [
    path('', index, name='forms'),
    path('<int:pk>/', OneFormsView.as_view(), name='form'),
    path('results/<int:pk>/', ResultsView.as_view(), name='results'),
]
