from rest_framework import serializers
from .models import Product, Category, Review, ProductImage, Wishlist, Promotion 

# creating a category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name']

#Creating review Serializer
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id','user','product','rating','comment','created_at']
        read_only_fields = ['user','created_at']
    #validate rating
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError('Rating must be between 1 and 5')
        return value
    
#Creating a ProductImage Serializer
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id','product','image_url']

#Creating a wishlist Serializer
class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ['id','user','product']

#Creating a promotion Serializer
class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ['id','product','discount_percentage','start_date','end_date']


#creating a product Serializer
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id','name','description','price','category','categories','image_url','stock_quantity','reviews','images','created_date']

    # Validating price and stock_quantity
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.") 
        return value
    #Reduce product stock by the purchased quantity
    def reduce_stock(self, product, quantity):
       if product.stock_quantity < quantity:
            raise serializers.ValidationError("Not enough stock available.")
       product.stock_quantity -= quantity
       product.save()
       return product

    def validate_stock_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError('stock quantity cannot be negative')
        return value

class PurchaseSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def validate(self, data):
        product = Product.objects.get(id=data['product_id'])
        if product.stock_quantity < data['quantity']:
            raise serializers.ValidationError("Not enough stock available")
        return data

    def update_stock(self, validated_data):
        product = Product.objects.get(id=validated_data['product_id'])
        product.stock_quantity -= validated_data['quantity']
        product.save()
        return product