from django.urls import path
from . import views

app_name = 'review'

urlpatterns = [ 
    path('add_review/<int:product_id>/<int:order_id>/', views.add_review, name='add_review'),
]