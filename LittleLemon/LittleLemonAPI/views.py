from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.paginator import *
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
    if request.method == 'GET':
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
        new_item = MenuItemSerializer(data=request.data)
        if new_item.is_valid():
            new_item.save()
            return Response({"message": "Item added into menu list"}, 201)
        else:   
            return Response({"message": "Bad request"}, 400)
    else:
        return Response({"message": "Unauthorized"}, 401)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def ThisItem(request, id):
    if request.method == 'GET':
        this_item = get_object_or_404(MenuItem, pk=id)
        this_item = MenuItemSerializer(this_item)
        return Response({"message": "Displaying this item"}, 200)
    elif request.method == 'PUT':
        this_item = get_object_or_404(MenuItem, pk=id)
        this_item = MenuItemSerializer(this_item)
        return Response({"message": "Updating this item"}, 200)
    elif request.method == 'PATCH':
        this_item = get_object_or_404(MenuItem, pk=id)
        this_item = MenuItemSerializer(this_item)
        return Response({"message": "Partially updating this item"}, 200)
    elif request.method == 'DELETE':
        this_item = get_object_or_404(MenuItem, pk=id)
        this_item = MenuItemSerializer(this_item)
        return Response({"message": "Deleting this item"}, 200)
    else:
        return Response({"message": "Unauthorized"}, 401)

@api_view(['GET', 'POST'])
def ViewManagers(request):
    if request.method == 'GET':
        return Response({"message": "Displaying manager list"}, 200)
    elif request.method == 'POST':
        new_manager = UserSerializer(data=request.data)
        if new_manager.is_valid():
            new_manager.save()
            return Response({"message": "New manager added"}, 201)
        else:   
            return Response({"message": "Bad request"}, 400)
    else:
        return Response({"message": "Unauthorized"}, 401)

@api_view(['DELETE'])
def RemoveManager(request, id):
    if request.method == 'DELETE':
        return Response({"message": "Deleting this manager"}, 200)
    else:
        return Response({"message": "Unauthorized"}, 401)

@api_view(['GET', 'POST'])
def ViewDeliveryCrew(request):
    if request.method == 'GET':
        return Response({"message": "Displaying delivery crew list"}, 200)
    elif request.method == 'POST':
        new_crew = UserSerializer(data=request.data)
        if new_crew.is_valid():
            new_crew.save()
            return Response({"message": "New delivery crew added"}, 201)
        else:   
            return Response({"message": "Bad request"}, 400)
    else:
        return Response({"message": "Unauthorized"}, 401)

@api_view(['DELETE'])
def RemoveDeliveryCrew(request, id):
    if request.method == 'DELETE':
        return Response({"message": "Deleting this delivery crew"}, 200)
    else:
        return Response({"message": "Unauthorized"}, 401)

@api_view(['GET', 'POST'])
def OrdersList(request):
    if request.method == 'GET':
        return Response({"message": "Displaying orders list"}, 200)
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
        this_order = get_object_or_404(Order, pk=id)
        this_order = OrderSerializer(this_order)
        return Response({"message": "Deleting this order"}, 200)
    else:
        return Response({"message": "Unauthorized"}, 401)

@api_view(['GET', 'POST', 'DELETE'])
def DisplayCart(request):
    if request.method == 'GET':
        return Response({"message": "Displaying cart"}, 200)
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

@permission_classes([IsAuthenticated])
def view_as_manager(request):
    if not request.user.groups.filter(name="Manager").exists():
        return Response({"message": "You do not have permission to perform this action."}, 403)

@permission_classes([IsAuthenticated])
def view_as_delivery_crew(request):
    if not request.user.groups.filter(name="Delivery crew").exists():
        return Response({"message": "You do not have permission to perform this action."}, 403)