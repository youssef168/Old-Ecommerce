from datetime import datetime

from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework import status


from .models import *
from .serializers import *

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_order(request):
    user = request.user
    data = request.data
    order_products = data['order_products']

    if order_products == None or len(order_products) == 0:
        error = {"message": "No Order Products Founded"}
        return Response(error, status=status.HTTP_400_BAD_REQUEST)
    else:
        order = Order.objects.create(
            user=user,
            paymentMethod=data.get('payment_method'),
            price=data.get('price'),
            shippingPrice=data.get('shippingPrice'),
            total=data.get('total'),
        )

        shipping_address = ShippingAddress.objects.create(
            order = order,
            city = data['shippingAdress']['city'],
            country = data['shippingAdress']['country'],
            address = data['shippingAdress']['address'],
            postal_code = data['shippingAdress']['postalCode'],
        )

        for i in order_products:
            product = Product.objects.get(_id=i['product'])

            item = OrderProduct.objects.create(
                product=product,
                order=order,
                price=i['price'],
                qty=i['qty'],
                name=product.name,
                image=product.img.url
            )

            product.stockCounter -= i['qty']
            product.save()

            serializer = OrderSerailizer(order, many=False)
            return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def get_orders(request):
    orders = Order.objects.all()
    serializer = OrderSerailizer(orders, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_myorders(request):
    user = request.user
    orders = user.order_set.all()
    serializer = OrderSerailizer(orders, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_orderby_id(request, id):
    user = request.user

    try:
        order = Order.objects.get(_id=id)
        if user.is_staff or order.user == user:
            serializer = OrderSerailizer(order, many=False)
            return Response(serializer.data)
        else:
            error = {"message": "Error In Authorized"}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
    except:
        error = {"message": "Order Does Not Exist"}
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_order_topaid(request, id):
    order = Order.objects.get(_id=id)
    user = request.user

    try:
        if user.is_staff or order.user == user:
            order.is_paid = True
            order.paid_at = datetime.now()
            order.save()
            serializer = OrderSerailizer(order, many=False)
            return Response(serializer.data)
        else:
            error = {"message": "Error In Authorized"}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
    except:
        error = {"message": "Order Does Not Exist"}
        return Response(error, status=status.HTTP_400_BAD_REQUEST)




@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_order_todelivered(request, id):
    order = Order.objects.get(_id=id)
    user = request.user
    
    try:
        if user.is_staff or order.user == user:
            order.is_deliverd  = True
            order.delivered_at = datetime.now()
            order.save()
            serializer = OrderSerailizer(order, many=False)
            return Response(serializer.data)
        else:
            error = {"message": "Error In Authorized"}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
    except:
        error = {"message": "Order Does Not Exist"}
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

            
