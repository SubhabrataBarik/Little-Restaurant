from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User, Group
from .models import MenuItem, Cart, Order, OrderItem
from .serializers import (MenuItemSerializer, CartSerializer, OrderSerializer)
from .permissions import IsManager, IsDeliveryCrew
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .paginations import DefaultPagination
from .filters import MenuItemFilter, OrderFilter

# ---------- MENU ITEMS ----------
class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = MenuItemFilter
    search_fields = ['title', 'category__title']
    ordering_fields = ['price', 'title']
    pagination_class = DefaultPagination

    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        return [IsAuthenticated(), IsManager()]

class SingleMenuItemsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        return [IsAuthenticated(), IsManager()]

# ---------- GROUP MANAGEMENT ----------
class ManagerUsersView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsManager]

    def get(self, request):
        users = User.objects.filter(groups__name='Manager')
        return Response(users.values('id', 'username'))

    def post(self, request):
        user = get_object_or_404(User, username=request.data.get('username'))
        managers = Group.objects.get(name='Manager')
        managers.user_set.add(user)
        return Response(status=status.HTTP_201_CREATED)

class ManagerUserDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsManager]

    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        managers = Group.objects.get(name='Manager')
        managers.user_set.remove(user)
        return Response(status=status.HTTP_200_OK)

class DeliveryCrewUsersView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsManager]

    def get(self, request):
        users = User.objects.filter(groups__name='Delivery crew')
        return Response(users.values('id', 'username'))

    def post(self, request):
        user = get_object_or_404(User, username=request.data.get('username'))
        crew = Group.objects.get(name='Delivery crew')
        crew.user_set.add(user)
        return Response(status=status.HTTP_201_CREATED)

# ---------- CART ----------
class CartView(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def delete(self, request):
        Cart.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_200_OK)
        
# ---------- ORDERS ----------
class OrdersView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = OrderFilter
    search_fields = ['user__username', 'delivery_crew__username']
    ordering_fields = ['date', 'total']
    pagination_class = DefaultPagination
    
    def get_queryset(self):
        if self.request.user.groups.filter(name='Manager').exists():
            return Order.objects.all()
        if self.request.user.groups.filter(name='Delivery crew').exists():
            return Order.objects.filter(delivery_crew=self.request.user)
        return Order.objects.filter(user=self.request.user)

    def post(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items.exists():
            return Response({'detail': 'Cart is empty'}, status=400)

        total = sum(item.price for item in cart_items)
        order = Order.objects.create(user=request.user, total=total)

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                menuitem=item.menuitem,
                quantity=item.quantity,
                unit_price=item.unit_price,
                price=item.price
            )

        cart_items.delete()
        return Response(OrderSerializer(order).data, status=201)

class SingleOrderView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]