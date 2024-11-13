from django.urls import path
from .views import (
    IndexView,
    AboutView,
    ContactView,
    FeaturesView,
    add_car,    
    car_list,
    car_detail,
    edit_car,
    delete_car
)

app_name = 'myapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('features/', FeaturesView.as_view(), name='features'),
    
    # Car Management URLs
    path('cars/', car_list, name='car_list'),                
    path('cars/add/', add_car, name='add_car'),             
    path('cars/<int:pk>/', car_detail, name='car_detail'),  
    path('cars/<int:pk>/edit/', edit_car, name='edit_car'),  
    path('cars/<int:pk>/delete/', delete_car, name='delete_car')
]
