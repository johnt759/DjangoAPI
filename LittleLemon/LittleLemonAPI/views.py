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
@permission_classes([IsAuthenticated])
def ItemsList(request):
    if request.method == 'GET':
        item_list = MenuItem.objects.all()
        which_category = request.query_params.get('category')
        which_title = request.query_params.get('title')
        keyword = request.query_params.get('search')
        if which_category is not None:
            item_list = item_list.filter(category__exact = which_category)
        if which_title is not None:
            item_list = item_list.filter(title__exact = which_title)
        if keyword is not None:
            item_list = item_list.filter(title__contains=keyword)
        item_list = MenuItemSerializer(item_list, many=True)
        return Response(item_list.data, 200)
    elif request.method == 'POST':
        if request.user.groups.filter(name="Manager").exists():
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
@permission_classes([IsAuthenticated])
def ThisItem(request, id):
    if request.method == 'GET':
        if request.user.groups.filter(name="Manager").exists():
            this_item = get_object_or_404(MenuItem, pk=id)
            this_item = MenuItemSerializer(this_item)
            return Response(this_item.data, 200)
        else:
            return Response({"message": "Forbidden"}, 403)
    elif request.method == 'PUT' or request.method == 'PATCH':
        if request.user.groups.filter(name="Manager").exists():
            this_item = get_object_or_404(MenuItem, pk=id)
            this_item = MenuItemSerializer(this_item, data=request.data)
            this_item.save()
            return Response({"message": "Item updated"}, 200)
        else:
            return Response({"message": "Forbidden"}, 403)
    elif request.method == 'DELETE':
        if request.user.groups.filter(name="Manager").exists():
            this_item = get_object_or_404(MenuItem, pk=id)
            this_item.delete()
            return Response({"message": "Item deleted"}, 200)
        else:
            return Response({"message": "Forbidden"}, 403)
    else:
        return Response({"message": "Unauthorized"}, 401)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def ViewManagers(request):
    if request.method == 'GET':
        if request.user.groups.filter(name="Manager").exists():
            manager_list = User.objects.all()
            manager_list = Group.objects.filter(name="Manager")
            manager_list = UserSerializer(manager_list, many=True)
            return Response(manager_list.data, 200)
        else:
            return Response({"message": "Forbidden"}, 403)
    elif request.method == 'POST':
        if request.user.groups.filter(name="Manager").exists():
            new_manager = get_object_or_404(User, username=request.data['username'])
            this_group = Group.objects.get(name="Manager")
            if new_manager not in this_group:
                this_group.user_set.add(new_manager)
                return Response({"message": "New manager added"}, 201)
            else:
                return Response({"message": "Manager already exists"}, 400)
        else:
            return Response({"message": "Forbidden"}, 403)
    else:
        return Response({"message": "Unauthorized"}, 401)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def RemoveManager(request, id):
    if request.method == 'DELETE':
        if request.user.groups.filter(name="Manager").exists():
            this_manager = get_object_or_404(User, pk=id)
            this_group = Group.objects.filter(name="Manager")
            if this_manager in this_group:
                this_group.user_set.remove(this_manager)
                return Response({"message": "Manager removed"}, 200)
            else:
                return Response({"message": "Unable to remove manager"}, 400)
        else:
            return Response({"message": "Forbidden"}, 403)
    else:
        return Response({"message": "Unauthorized"}, 401)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def ViewDeliveryCrew(request):
    if request.method == 'GET':
        if request.user.groups.filter(name="Manager").exists():
            crew_list = User.objects.all()
            crew_list = Group.objects.filter(name="Delivery Crew")
            crew_list = UserSerializer(crew_list, many=True)
            return Response(crew_list.data, 200)
        else:
            return Response({"message": "Forbidden"}, 403)
    elif request.method == 'POST':
        if request.user.groups.filter(name="Manager").exists():
            new_crew = get_object_or_404(User, username=request.data['username'])
            this_group = Group.objects.get(name="Delivery Crew")
            if new_crew not in this_group:
                this_group.user_set.add(new_crew)
                return Response({"message": "New delivery crew added"}, 201)
            else:
                return Response({"message": "Delivery crew already exists"}, 400)
        else:
            return Response({"message": "Forbidden"}, 403)
    else:
        return Response({"message": "Unauthorized"}, 401)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def RemoveDeliveryCrew(request, id):
    if request.method == 'DELETE':
        if request.user.groups.filter(name="Manager").exists():
            this_crew = get_object_or_404(User, pk=id)
            this_group = Group.objects.filter(name="Delivery Crew")
            if this_crew in this_group:
                this_group.user_set.remove(this_crew)
                return Response({"message": "Delivery crew removed"}, 200)
            else:
                return Response({"message": "Unable to remove delivery crew"}, 400)
        else:
            return Response({"message": "Forbidden"}, 403)
    else:
        return Response({"message": "Unauthorized"}, 401)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def OrdersList(request):
    if request.method == 'GET':
        order_list = Order.objects.all()
        order_list = OrderSerializer(order_list, many=True)
        return Response(order_list.data, 200)
    elif request.method == 'POST':
        new_order = OrderSerializer(data=request.data)
        if new_order.is_valid():
            new_order.save()
            return Response({"message": "New order added"}, 201)
        else:
            return Response({"message": "Bad request"}, 400)
    else:
        return Response({"message": "Unauthorized"}, 401)

@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def ThisOrder(request, id):
    if request.method == 'GET':
        this_order = get_object_or_404(Order, pk=id)
        this_order = OrderSerializer(this_order)
        return Response(this_order.data, 200)
    elif request.method == 'PATCH' or request.method == 'PUT':
        if request.user.groups.filter(name="Manager").exists() or request.user.groups.filter(name="Delivery Crew").exists():
            this_order = get_object_or_404(Order, pk=id)
            this_order = OrderSerializer(this_order, data=request.data)
            this_order.save()
            return Response({"message": "Order status updated"}, 200)
        else:
            return Response({"message": "Forbidden"}, 403)
    elif request.method == 'DELETE':
        if request.user.groups.filter(name="Manager").exists():
            this_order = get_object_or_404(Order, pk=id)
            this_order.delete()
            return Response({"message": "Order deleted"}, 200)
        else:
            return Response({"message": "Forbidden"}, 403)
    else:
        return Response({"message": "Unauthorized"}, 401)

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def DisplayCart(request):
    if request.method == 'GET':
        this_cart = Cart.objects.all()
        this_cart = CartSerializer(this_cart, many=True)
        return Response(this_cart.data, 200)
    elif request.method == 'POST':
        new_cart = CartSerializer(data=request.data)
        if new_cart.is_valid():
            new_cart.save()
            return Response({"message": "New item added to cart"}, 201)
        else:
            return Response({"message": "Bad request"}, 400)
    elif request.method == 'DELETE':
        this_cart = Cart.objects.all()
        this_cart.delete()
        return Response({"message": "Emptying cart"}, 200)
    else:
        return Response({"message": "Unauthorized"}, 401)