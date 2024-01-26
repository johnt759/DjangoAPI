from django.urls import path
from . import views

urlpatterns = [
    path('menu-items', views.ItemsList),
    path('menu-items/<int:id>', views.ThisItem),
    path('groups/manager/users', views.ViewManagers),
    path('groups/manager/users/<int:id>', views.RemoveManager),
    path('groups/delivery-crew/users', views.ViewDeliveryCrew),
    path('groups/delivery-crew/users/<int:id>', views.RemoveDeliveryCrew),
    path('cart/menu-items', views.DisplayCart),
    path('orders', views.OrdersList),
    path('orders/<int:id>', views.ThisOrder),
]