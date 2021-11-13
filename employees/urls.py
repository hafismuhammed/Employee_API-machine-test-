from django.urls import path
from . import views

urlpatterns = [
    path('all-employees/', views.ListEmployeesAPIView.as_view(), name='all_employees'),
    path('add-employees/', views.AddEmployeesAPIView.as_view(), name='add_employees'),
]