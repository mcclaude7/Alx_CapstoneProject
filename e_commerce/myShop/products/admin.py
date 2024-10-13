from django.contrib import admin
from .models import Product, Category, Review, Wishlist, ProductImage, Promotion

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Wishlist)
admin.site.register(ProductImage)
admin.site.register(Promotion)