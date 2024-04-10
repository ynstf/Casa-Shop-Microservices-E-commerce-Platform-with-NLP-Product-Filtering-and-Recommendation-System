from . import views
from django.urls import path

urlpatterns = [
    path('showproducts', views.product_list),
    path('all_cate', views.all_categories),
    path('showproducts/<int:pk>/', views.product_show),
    path('productcategories/<int:pk>/', views.product_categories),
    path('postproducts', views.product_create),

]