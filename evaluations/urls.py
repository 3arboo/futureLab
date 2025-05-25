from django.urls import path
from . import views

app_name = 'evaluations'

urlpatterns = [
    path('', views.evaluation_list, name='evaluation_list'),
    path('<int:pk>/', views.evaluation_detail, name='evaluation_detail'),
]