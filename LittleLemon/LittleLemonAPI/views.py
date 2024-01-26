from django.shortcuts import get_object_or_404
from django.core.paginator import *
from django.contrib.auth.models import User, Group
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.decorators import *
from djoser import *
from .models import *
from .serializers import *

# Create your views here.
@api_view(['GET', 'POST'])
def ItemsList(request):
    if request.method == 'GET' and request.user.isAuthenticated():
        item_list = MenuItem.objects.all()
        which_category = request.query_params.get('category')
        which_title = request.query_params.get('title')
        keyword = request.query_params.get('search')
        if which_category:
            item_list = item_list.filter(category__exact = which_category)
        if which_title:
            item_list = item_list.filter(title__exact = which_title)
        if keyword:
            item_list = item_list.filter(title__contains=keyword)
        item_list = MenuItemSerializer(item_list, many=True)
        return Response({"message": "Displaying all items from list"}, 200)
    elif request.method == 'POST':
        if request.user.isAuthenticated() and request.user.groups.filter(name="Manager").exists():
            new_item = MenuItemSerializer(data=request.data)
            if new_item.is_valid():
                new_item.save()
                return Response({"message": "Item added into menu list"}, 201)
            else:   
                return Response({"message": "Bad request"}, 400)
        else:
            return Response({"message": "Forbidden"}, 403)
    else:
        return Response({"message": "Unauthorized"}, 401)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def ThisItem(request, id):
    if request.method == 'GET':
        if request.user.isAuthenticated() and request.user.groups.filter(name="Manager").exists():
            this_item = get_object_or_404(MenuItem, pk=id)
            this_item = MenuItemSerializer(this_item)
            return Response({"message": "Displaying this item"}, 200)
        else:
            return Response({"message": "Forbidden"}, 403)
    elif request.method == 'PUT':
        if request.user.isAuthenticated() and request.user.groups.filter(name="Manager").exists():
            this_item = get_object_or_404(MenuItem, pk=id)
            this_item = MenuItemSerializer(this_item)
            return Response({"message": "Updating this item"}, 200)
        else:
            return Response({"message": "Forbidden"}, 403)
    elif request.method == 'PATCH':
        if request.user.isAuthenticated() and request.user.groups.filter(name="Manager").exists():
            this_item = get_object_or_404(MenuItem, pk=id)
            this_item = MenuItemSerializer(this_item)
            return Response({"message": "Partially updating this item"}, 200)
        else:
            return Response({"message": "Forbidden"}, 403)
    elif request.method == 'DELETE':
        if request.user.isAuthenticated() and request.user.groups.filter(name="Manager").exists():
            this_item = get_object_or_404(MenuItem, pk=id)
            this_item.delete()
            return Response({"message": "Item deleted"}, 200)
        else:
            return Response({"message": "Forbidden"}, 403)
    else:
        return Response({"message": "Unauthorized"}, 401)

@api_view(['GET', 'POST'])
def ViewManagers(request):
    if request.method == 'GET':
        if request.user.groups.filter(name="Manager").exists() and request.user.isAuthenticated():
            manager_list = User.objects.all()
            manager_list = Group.objects.filter(name="Manager")
            manager_list = UserSerializer(manager_list, many=True)
            return Response(manager_list, 200)
        else:
            return Response({"message": "Forbidden"}, 403)
    elif request.method == 'POST':
        if request.user.groups.filter(name="Manager").exists() and request.user.isAuthenticated():
            new_manager = UserSerializer(data=request.data)
            if new_manager.is_valid():
                this_group = Group.objects.filter(name="Manager")
                this_group.user_set.add(new_manager)
                return Response({"message": "New manager added"}, 201)
            else:   
                return Response({"message": "Bad request"}, 400)
        else:
            return Response({"message": "Forbidden"}, 403)
    else:
        return Response({"message": "Unauthorized"}, 401)

@api_view(['DELETE'])
def RemoveManager(request, id):
    if request.method == 'DELETE':
        if request.user.groups.filter(name="Manager").exists() and request.user.isAuthenticated():
            this_manager = get_object_or_404(User, pk=id)
            this_manager = Group.objects.filter(name="Manager")
            this_manager.delete()
            return Response({"message": "Manager removed"}, 200)
        else:
            return Response({"message": "Forbidden"}, 403)
    else:
        return Response({"message": "Unauthorized"}, 401)

@api_view(['GET', 'POST'])
def ViewDeliveryCrew(request):
    if request.method == 'GET':
        if request.user.groups.filter(name="Manager").exists() and request.user.isAuthenticated():
            crew_list = User.objects.all()
            crew_list = Group.objects.filter(name="Delivery Crew")
            crew_list = UserSerializer(crew_list, many=True)
            return Response(crew_list, 200)
        else:
            return Response({"message": "Forbidden"}, 403)
    elif request.method == 'POST':
        if request.user.groups.filter(name="Manager").exists() and request.user.isAuthenticated():
            new_crew = UserSerializer(data=request.data)
            if new_crew.is_valid():
                this_group = Group.objects.filter(name="Delivery Crew")
                this_group.user_set.add(new_crew)
                return Response({"message": "New delivery crew added"}, 201)
            else:   
                return Response({"message": "Bad request"}, 400)
        else:
            return Response({"message": "Forbidden"}, 403)
    else:
        return Response({"message": "Unauthorized"}, 401)

@api_view(['DELETE'])
def RemoveDeliveryCrew(request, id):
    if request.method == 'DELETE':
        if request.user.groups.filter(name="Manager").exists() and request.user.isAuthenticated():
            this_crew = get_object_or_404(User, pk=id)
            this_crew = Group.objects.filter(name="Delivery Crew")
            this_crew.delete()
            return Response({"message": "Delivery crew removed"}, 200)
        else:
            return Response({"message": "Forbidden"}, 403)
    else:
        return Response({"message": "Unauthorized"}, 401)

@api_view(['GET', 'POST'])
def OrdersList(request):
    if request.method == 'GET':
        order_list = Order.objects.all()
        order_list = OrderSerializer(order_list, many=True)
        return Response(order_list, 200)
    elif request.method == 'POST':
        new_order = OrderSerializer(data=request.data)
        if new_order.is_valid():
            new_order.save()
            return Response({"message": "New order added"}, 201)
        else:   
            return Response({"message": "Bad request"}, 400)
    else:
        return Response({"message": "Unauthorized"}, 401)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def ThisOrder(request, id):
    if request.method == 'GET':
        this_order = get_object_or_404(Order, pk=id)
        this_order = OrderSerializer(this_order)
        return Response({"message": "Displaying this order"}, 200)
    elif request.method == 'PUT':
        this_order = get_object_or_404(Order, pk=id)
        this_order = OrderSerializer(this_order)
        return Response({"message": "Updating this order"}, 200)
    elif request.method == 'PATCH':
        this_order = get_object_or_404(Order, pk=id)
        this_order = OrderSerializer(this_order)
        return Response({"message": "Partially updating this order"}, 200)
    elif request.method == 'DELETE':
        if request.user.groups.filter(name="Manager").exists() and request.user.isAuthenticated():
            this_order = get_object_or_404(Order, pk=id)
            this_order = OrderSerializer(this_order)
            return Response({"message": "Deleting this order"}, 200)
        else:
            return Response({"message": "Forbidden"}, 403)
    else:
        return Response({"message": "Unauthorized"}, 401)

@api_view(['GET', 'POST', 'DELETE'])
def DisplayCart(request):
    if request.method == 'GET':
        this_cart = Cart.objects.all()
        this_cart = CartSerializer(this_cart, many=True)
        return Response(this_cart, 200)
    elif request.method == 'POST':
        new_cart = CartSerializer(data=request.data)
        if new_cart.is_valid():
            new_cart.save()
            return Response({"message": "New item added to cart"}, 201)
        else:   
            return Response({"message": "Bad request"}, 400)
    elif request.method == 'DELETE':
        return Response({"message": "Emptying cart"}, 200)
    else:
        return Response({"message": "Unauthorized"}, 401)

# The following functions below shall indicate whether the user is autheticated to access,
# and if the following actions can be done only by a manager or delivery crew.

@permission_classes([IsAuthenticated])
def view_as_manager(request):
    if not request.user.groups.filter(name="Manager").exists() and request.user.IsAuthenticated():
        return Response({"message": "You do not have permission to perform this action."}, 403)

@permission_classes([IsAuthenticated])
def view_as_delivery_crew(request):
    if not request.user.groups.filter(name="Delivery crew").exists() and request.user.IsAuthenticated():
        return Response({"message": "You do not have permission to perform this action."}, 403)