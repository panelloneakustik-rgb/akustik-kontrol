from rest_framework import serializers
from .models import Category, Product, ProductImage, HeroSlide, ColorSwatch, Review, Story


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "icon", "order"]


class ColorSwatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorSwatch
        fields = ["id", "code", "name", "image"]


class HeroSlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroSlide
        fields = ["id", "image", "badge_text", "title", "subtitle", "cta_text", "cta_link", "order"]

class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ["id", "title", "image", "link_url", "order"]        


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    is_verified_purchase = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ["id", "user_name", "rating", "comment", "is_verified_purchase", "created_at"]

    def get_user_name(self, obj):
        full_name = f"{obj.user.first_name} {obj.user.last_name}".strip()
        if full_name:
            parts = full_name.split(" ")
            if len(parts) > 1:
                return f"{parts[0]} {parts[-1][0]}."
            return parts[0]
        return obj.user.email.split("@")[0]

    def get_is_verified_purchase(self, obj):
        from orders.models import Order
        return Order.objects.filter(
            user=obj.user, items__product=obj.product, status__in=["paid", "shipped", "delivered"]
        ).exists()


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image", "order"]


class ProductListSerializer(serializers.ModelSerializer):
    """Compact shape used on the product-grid / bestsellers cards."""
    category = serializers.SlugRelatedField(slug_field="slug", read_only=True)
    discounted_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    gallery_images = ProductImageSerializer(many=True, read_only=True)
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id", "name", "slug", "category", "image", "images", "gallery_images",
            "price", "discount_percent", "discounted_price",
            "is_new", "is_bestseller", "stock",
        ]

    def get_images(self, obj):
        request = self.context.get("request")
        urls = []
        if obj.image:
            urls.append(request.build_absolute_uri(obj.image.url) if request else obj.image.url)
        for gi in obj.gallery_images.all():
            urls.append(request.build_absolute_uri(gi.image.url) if request else gi.image.url)
        return urls


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    discounted_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    gallery_images = ProductImageSerializer(many=True, read_only=True)
    images = serializers.SerializerMethodField()
    related_products = serializers.SerializerMethodField()
    color_swatches = ColorSwatchSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id", "name", "slug", "category", "description", "image", "images", "gallery_images",
            "price", "discount_percent", "discounted_price",
            "is_new", "is_bestseller", "stock",
            "dimensions", "material", "color", "color_swatches",
            "average_rating", "review_count",
            "related_products",
        ]

    def get_images(self, obj):
        request = self.context.get("request")
        urls = []
        if obj.image:
            urls.append(request.build_absolute_uri(obj.image.url) if request else obj.image.url)
        for gi in obj.gallery_images.all():
            urls.append(request.build_absolute_uri(gi.image.url) if request else gi.image.url)
        return urls

    def get_related_products(self, obj):
        qs = Product.objects.filter(category=obj.category).exclude(pk=obj.pk).select_related("category")[:4]
        return ProductListSerializer(qs, many=True, context=self.context).data

    def get_average_rating(self, obj):
        approved = obj.reviews.filter(is_approved=True)
        if not approved.exists():
            return None
        return round(sum(r.rating for r in approved) / approved.count(), 1)

    def get_review_count(self, obj):
        return obj.reviews.filter(is_approved=True).count()