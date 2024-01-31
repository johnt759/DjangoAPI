from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth.models import User, Group
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import *
from djoser import *
from .models import *
from .serializers import *
from datetime import date

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
            new_name = request.data['title']
            new_price = request.data['price']
            new_featured = request.data['featured']
            new_category = request.data['category']
            category_id = Category.objects.get(title=new_category)
            new_item = MenuItem(title=new_name, price=new_price, featured=new_featured, category=category_id)
            new_item.save()
            return Response({"message": "Item added into menu list"}, 201)
        else:
            return Response({"message": "Forbidden"}, 403)
    else:
        return Response({"message": "Unknown Method"}, 405)

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
    elif request.method == 'PUT':
        if request.user.groups.filter(name="Manager").exists():
            this_item = get_object_or_404(MenuItem, pk=id)
            this_title = request.data['title']
            this_price = request.data['price']
            this_category = request.data['category']
            if this_item:
                this_item.title = this_title
            if this_title:
                this_item.price = this_price
            if this_category:
                category_id = Category.objects.get(title=this_category)
                this_item.category = category_id
            this_item.save()
            return Response({"message": "Item updated"}, 200)
        else:
            return Response({"message": "Forbidden"}, 403)
    elif request.method == 'PATCH':
        if request.user.groups.filter(name="Manager").exists():
            this_item = get_object_or_404(MenuItem, pk=id)
            this_item.featured = not this_item.featured
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
        return Response({"message": "Unknown Method"}, 405)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def ViewManagers(request):
    if request.method == 'GET':
        if request.user.groups.filter(name="Manager").exists():
            manager_list = User.objects.all().filter(groups__name="Manager")
            manager_list = UserSerializer(manager_list, many=True)
            return Response(manager_list.data, 200)
        else:
            return Response({"message": "Forbidden"}, 403)
    elif request.method == 'POST':
        if request.user.groups.filter(name="Manager").exists():
            new_manager = User.objects.get(username=request.data['username'])
            this_group = Group.objects.get(name__contains="Manager")
            if not new_manager.groups.filter(name="Manager").exists():
                this_group.user_set.add(new_manager)
                return Response({"message": "New manager added"}, 201)
            else:
                return Response({"message": "Manager already exists"}, 400)
        else:
            return Response({"message": "Forbidden"}, 403)
    else:
        return Response({"message": "Unknown Method"}, 405)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def RemoveManager(request, id):
    if request.method == 'DELETE':
        if request.user.groups.filter(name="Manager").exists():
            this_manager = get_object_or_404(User, pk=id)
            this_group = Group.objects.all().filter(name__contains="Manager")
            if this_manager.groups.filter(name="Manager").exists():
                this_group.user_set.remove(this_manager)
                return Response({"message": "Manager removed"}, 200)
            else:
                return Response({"message": "Manager doesn't exist"}, 400)
        else:
            return Response({"message": "Forbidden"}, 403)
    else:
        return Response({"message": "Unknown Method"}, 405)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def ViewDeliveryCrew(request):
    if request.method == 'GET':
        if request.user.groups.filter(name="Manager").exists():
            crew_list = User.objects.all().filter(groups__name="Delivery Crew")
            crew_list = UserSerializer(crew_list, many=True)
            return Response(crew_list.data, 200)
        else:
            return Response({"message": "Forbidden"}, 403)
    elif request.method == 'POST':
        if request.user.groups.filter(name="Manager").exists():
            new_crew = User.objects.get(username=request.data['username'])
            this_group = Group.objects.get(name__contains="Delivery Crew")
            if not new_crew.groups.filter(name="Delivery Crew").exists():
                this_group.user_set.add(new_crew)
                return Response({"message": "New delivery crew added"}, 201)
            else:
                return Response({"message": "Delivery crew already exists"}, 400)
        else:
            return Response({"message": "Forbidden"}, 403)
    else:
        return Response({"message": "Unknown Method"}, 405)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def RemoveDeliveryCrew(request, id):
    if request.method == 'DELETE':
        if request.user.groups.filter(name="Manager").exists():
            this_crew = get_object_or_404(User, pk=id)
            this_group = Group.objects.get(name__contains="Delivery Crew")
            if this_crew.groups.filter(name="Delivery Crew").exists():
                this_group.user_set.remove(this_crew)
                return Response({"message": "Delivery crew removed"}, 200)
            else:
                return Response({"message": "Delivery crew doesn't exist"}, 400)
        else:
            return Response({"message": "Forbidden"}, 403)
    else:
        return Response({"message": "Unknown Method"}, 405)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def OrdersList(request):
    if request.method == 'GET':
        order_list = OrderItem.objects.all()
        order_list = OrderItemSerializer(order_list, many=True)
        return Response(order_list.data, 200)
    elif request.method == 'POST':
        order_total = 0
        this_user = get_object_or_404(User, id=request.user.id)
        this_cart = get_list_or_404(Cart, user=this_user)
        for this_item in this_cart:
            new_order_item = OrderItem(order=this_item.user, menuitem=this_item.menuitem,
                                  quantity=this_item.quantity, unit_price = this_item.unit_price,
                                  price=this_item.price)
            new_order_item.save()
        for this_item in this_cart:
            order_total += float(this_item.price)
        new_order = Order(order=this_user, total=order_total, date=date.today())
        new_order.save()
        for this_item in this_cart:
            this_item.delete()
        return Response({"message": "New order placed"}, 201)
    else:
        return Response({"message": "Unknown Method"}, 405)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def ThisOrder(request, id):
    if request.method == 'GET':
        if request.user.groups.filter(name="Manager").exists():
            this_order = Order.objects.all()
            this_order = OrderSerializer(this_order, many=True)
            return Response(this_order.data, 200)
        else:
            this_user = get_object_or_404(User, id=request.user.id)
            this_order = Order.objects.all().filter(user=this_user.id)
            if not this_order:
                return Response({"message": "User doesn't exist"}, 404)
            this_order = OrderSerializer(this_order, many=True)
            return Response(this_order.data, 200)
    elif request.method == 'PUT':
        if request.user.groups.filter(name="Manager").exists():
            this_order = get_object_or_404(Order, pk=id)
            this_crew = get_object_or_404(User, username=request.data['delivery_crew'])
            if this_crew.groups.filter(name="Delivery Crew").exists():
                this_order.delivery_crew = this_crew
                this_order.save()
                return Response({"message": "Order status updated"}, 200)
            else:
                return Response({"message": "Delivery crew doesn't exist"}, 404)
        else:
            return Response({"message": "Forbidden"}, 403)
    elif request.method == 'PATCH':
        if request.user.groups.filter(name="Manager").exists() or request.user.groups.filter(name="Delivery Crew").exists():
            this_order = get_object_or_404(Order, pk=id)
            this_order.status = not this_order.status
            this_order.save()
            return Response({"message": "Order status updated"}, 200)
        else:
            return Response({"message": "Forbidden"}, 403)
    elif request.method == 'DELETE':
        if request.user.groups.filter(name="Manager").exists():
            this_order = get_object_or_404(Order, pk=id)
            user_id = this_order.user
            this_user = get_object_or_404(User, id=user_id)
            order_items = get_list_or_404(OrderItem, order=this_user)
            for this_item in order_items:
                this_item.delete()
            this_order.delete()    
            return Response({"message": "Order deleted"}, 200)
        else:
            return Response({"message": "Forbidden"}, 403)
    else:
        return Response({"message": "Unknown Method"}, 405)

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def DisplayCart(request):
    this_user = request.user.id
    if request.method == 'GET':
        this_cart = Cart.objects.all().filter(user=this_user)
        if not this_cart:
            return Response({"message": "Cart is empty"}, 404)
        this_cart = CartSerializer(this_cart, many=True)
        return Response(this_cart.data, 200)
    elif request.method == 'POST':
        item_name = request.data['menuitem']
        num_ordered = int(request.data['quantity'])
        this_item = get_object_or_404(MenuItem, title=item_name)
        this_item = MenuItemSerializer2(this_item)
        this_price = float(this_item.data['price'])
        total_price = num_ordered*this_price
        user_id = User.objects.get(id=this_user)
        item_name = MenuItem.objects.get(title=request.data['menuitem'])
        new_item = Cart(user=user_id, menuitem=item_name,
                        quantity=num_ordered, unit_price=this_price,
                        price=total_price)
        new_item.save()
        return Response({"message": "New item added to cart"}, 201)
    elif request.method == 'DELETE':
        this_cart = Cart.objects.all().filter(user=this_user)
        this_cart.delete()
        return Response({"message": "Emptying cart"}, 200)
    else:
        return Response({"message": "Unknown Method"}, 405)