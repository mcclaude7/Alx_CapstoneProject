from django.shortcuts import render
from rest_framework import viewsets, filters
from .models import Product, Category, Review, ProductImage, Wishlist, Promotion, User
from .serializers import ProductSerializer, CategorySerializer, ProductImageSerializer, PurchaseSerializer, PromotionSerializer, ReviewSerializer, WishlistSerializer 
from rest_framework.decorators import action 
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from django.views.generic import TemplateView

#Product viewsets
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    #permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def purchase(self, request, pk=None):
        
        product = self.get_object()  # Get the product by its ID
        quantity = request.data.get('quantity', 1)  # Get the purchase quantity (default is 1)
        try:
            quantity = int(quantity)
        except ValueError:
            return Response({"error": "Quantity must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate quantity
        if quantity <= 0:
            return Response({"error": "Quantity must be greater than zero."}, status=status.HTTP_400_BAD_REQUEST)

        # reduce stock using serializer
        serializer = self.get_serializer()
        try:
            product = serializer.reduce_stock(product, quantity)
        except serializers.ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Return product details with updated stock quantity
        return Response({
            "message": f"You have successfully purchased {quantity} of {product.name}.",
            "remaining_stock": product.stock_quantity,
            "product_details": ProductSerializer(product).data
        }, status=status.HTTP_200_OK)

    # Add filtering, search, and pagination capabilities
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'category__name'] # Enable searching by 'name' and 'category'
    # Filtering products by price range and stock availability
    filterset_fields = {
        'price': ['gte', 'lte'],  # Filter by min_price and max_price
        'stock_quantity': ['gt']  # Filter by stock availability
    }
    # Optional: Enable ordering by fields (e.g., price, name)
    ordering_fields = ['price', 'name']
    ordering = ['name']  # Default ordering


#Category viewsets
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    #permission_classes = [permissions.IsAuthenticated]

#Review viewsets
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    #permission_classes =[permissions.IsAuthenticated] 

    #Associate the review with the logged-in user
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    #Allow only the creator of the review to update or delete it
    def get_permissions(self):
        if self.action in ['update', 'partial_update','destoy']:
             review = self.get_object()
             if review.user != self.request.user:
                 raise PermissionDenied("You don't have permission to modify this review.")
        return super().get_permissions()

#ProductImage viewsets    
class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    #permission_classes = [permissions.IsAuthenticated]

#Wishlist viewsets
class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    #permission_classes = IsAuthenticated

#Promotion viewsets
class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    #permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class APIDocumentationView(TemplateView):
    template_name = 'v1/documentation.html'