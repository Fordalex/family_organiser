from django.urls import path
from . import views

urlpatterns = [
    path('shopping_page', views.shopping_page, name="shopping_page"),
    path('add_item', views.add_item, name="add_item"),
    path('update_category/<operation>/<pk>', views.update_category, name="update_category"),
]