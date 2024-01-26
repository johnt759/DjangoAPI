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
        return Response("Displaying items list")
    elif request.method == 'POST':
        return Response("Adding item into the list")
    else:
        return Response({"message": "Invalid request"}, 400)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def ThisItem(request, id):
    if request.method == 'GET':
        return Response("Displaying item of id ", id)
    elif request.method == 'PUT':
        return Response("Updating item of id ", id)
    elif request.method == 'PATCH':
        return Response("Partially updating item of id ", id)
    elif request.method == 'DELETE':
        return Response("Deleting item of id ", id)
    else:
        return Response({"message": "Invalid request"}, 400)

@api_view(['GET', 'POST'])
def ViewManagers(request):
    if request.method == 'GET':
        return Response("Displaying all managers")
    elif request.method == 'POST':
        return Response("Adding new manager")
    else:
        return Response({"message": "Invalid request"}, 400)

@api_view(['DELETE'])
def RemoveManager(request, id):
    if request.method == 'DELETE':
        return Response("Removing manager of id ", id)
    else:
        return Response({"message": "Invalid request"}, 400)

@api_view(['GET', 'POST'])
def ViewDeliveryCrew(request):
    if request.method == 'GET':
        return Response("Displaying all delivery crew members")
    elif request.method == 'POST':
        return Response("Adding new delivery crew member")
    else:
        return Response({"message": "Invalid request"}, 400)

@api_view(['DELETE'])
def RemoveDeliveryCrew(request, id):
    if request.method == 'DELETE':
        return Response("Removing delivery crew member of id ", id)
    else:
        return Response({"message": "Invalid request"}, 400)

@api_view(['GET', 'POST'])
def OrdersList(request):
    if request.method == 'GET':
        return Response("Displaying orders list")
    elif request.method == 'POST':
        return Response("Creating new order")
    else:
        return Response({"message": "Invalid request"}, 400)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def ThisOrder(request, id):
    if request.method == 'GET':
        return Response("Displaying items for order id ", id)
    elif request.method == 'PUT':
        return Response("Updating status for order id ", id)
    elif request.method == 'PATCH':
        return Response("Partially updating status for order id ", id)
    elif request.method == 'DELETE':
        return Response("Deleting order for order id ", id)
    else:
        return Response({"message": "Invalid request"}, 400)

@api_view(['GET', 'POST', 'DELETE'])
def DisplayCart(request):
    if request.method == 'GET':
        return Response("Displaying cart")
    elif request.method == 'POST':
        return Response("Adding item into the cart")
    elif request.method == 'DELETE':
        return Response("Emptying the cart")
    else:
        return Response({"message": "Invalid request"}, 400)

@permission_classes([IsAuthenticated])
def view_as_manager(request):
    if not request.user.groups.filter(name="Manager").exists():
        return Response({"message": "You do not have permission to perform this action."}, 403)

@permission_classes([IsAuthenticated])
def view_as_delivery_crew(request):
    if not request.user.groups.filter(name="Delivery crew").exists():
        return Response({"message": "You do not have permission to perform this action."}, 403)