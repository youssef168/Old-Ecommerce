#From Django's Core
from django.core import paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#From REST
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import permissions, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework import status

# From Local
from src.models import *
from src.serializers import ProductSerializer, UserSerializer

#Views Logic

#TODO Get All Products And Serialize It

@permission_classes([permissions.AllowAny])
@api_view(['GET'])
def getProducts(request):
    query_param = request.query_params.get('keyword')
    if query_param == None or query_param == '':
        query_param = ''
    
    products = Product.objects.filter(product_name__icontains=query_param).order_by('-_id')
    page = request.query_params.get('page')
    paginator = Paginator(products, 7)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    if page == None:
        page = 1
    page = int(page)

    serializers = ProductSerializer(products, many=True)
    return Response({'products': serializers.data, 'page': page, 'page_total': paginator.num_pages})

#TODO Get One Product Based On ID
@api_view(['GET'])
def getProduct(request, id):
    product = Product.objects.get(_id=id)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


#TODO Get Top Rated Product
@api_view(['GET'])
def get_top_rated_product(request):
    product = Product.objects.filter(rating__gte=3).order_by('-rating')
    serializer = ProductSerializer(product, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_best_rated_product(request):
    product = Product.objects.filter(rating=5)[:1]
    serializer = ProductSerializer(product, many=True)
    return Response(serializer.data)

# @api_view(['GET'])
# # @permission_classes([permissions.IsAdminUser])
# def create_product(self,request):
#     user = request.user
#     serializer = UserSerializer(user, many=False)
#     return Response(serializer.data)

# class GetCurrentUser(APIView):
#     authentication_classes = (BasicAuthentication, JSONWebTokenAuthentication)
#     def get(self, request):
#         serializer = UserSerializer(request.user)
#         return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def create_product(request):
    user = request.user
    data = request.data

    product = Product.objects.create(
        owner=user,
        product_name= data['product_name'],
        price= data['price'],
        product_brand= data['product_brand'],
        stockCounter= data['stockCounter'],
        category= data['category'],
        description= data['description']
    )

    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([permissions.IsAdminUser])
def update_product(request, id):
    product = Product.objects.get(_id=id)

    data = request.data

    product.price = data.get('price')
    product.product_name = data.get('product_name')
    product.product_img = data.get('product_img')
    product.product_brand = data.get('product_brand')
    product.description = data.get('description')
    product.stockCounter = data.get('stockCounter')
    product.category = data.get('category')
    
    product.save()

    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([permissions.IsAdminUser])
def delete_product(request, id):
    product = Product.objects.get(_id=id)
    product.delete()
    return Response("Product Deleted Successfully")


@api_view(['GET'])
# @permission_classes([permissions.IsAuthenticated])
def create_product_review(request, id):
    user = request.user
    product = Product.objects.get(_id=id)
    data = request.data

    exist_review = product.review_set.get(user=user)

    # if exist_review:
    #     error = {"Error": "Review On This Product Already Exist"}
    #     return Response(error, status=status.HTTP_400_BAD_REQUEST)

    # elif data.get('rating') == 0:
    #     error = {"Error": "Please Select Rating!"}
    #     return Response(error, status=status.HTTP_400_BAD_REQUEST)
    # else:
    #     productSerializer = ProductSerializer(product)
    #     return Response(productSerializer.data)

    productSerializer = ProductSerializer(product)
    return Response(productSerializer.data)
    
    # else:
    #     review = Review.objects.create(
    #         user = user,
    #         product = product,
    #         rating = data.get('rating'),
    #         description = data.get('description')
    #     )

    #     reviews = product.review_set.all()

    #     product.review_count = len(reviews)

    #     total = 0

    #     for i in reviews:
    #         total = i.rating
    #     product.rating = total / len(reviews)
    #     product.save()

    #     return Response("Review Have Been Added Successfully")
    
