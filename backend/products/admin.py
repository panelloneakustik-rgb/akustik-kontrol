from django.contrib import admin
from .models import Category, Product, ProductImage, Favorite, Story,HeroSlide,ColorSwatch, Review
from django.utils.html import format_html

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(ColorSwatch)
class ColorSwatchAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "preview")
    search_fields = ("code", "name")

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:32px;height:32px;object-fit:cover;border-radius:4px;" />', obj.image.url)
        return "-"
    preview.short_description = "Önizleme"


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "discount_percent", "discounted_price", "is_new", "is_bestseller", "stock")
    list_filter = ("category", "is_new", "is_bestseller")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("color_swatches",)
    inlines = [ProductImageInline]
    fieldsets = (
        (None, {"fields": ("category", "name", "slug", "description", "image")}),
        ("Fiyat", {"fields": ("price", "discount_percent")}),
        ("Teknik Özellikler", {"fields": ("dimensions", "material", "color")}),
        ("Durum", {"fields": ("is_new", "is_bestseller", "stock")}),
        ("Renk Seçenekleri", {"fields": ("color_swatches",), "description": "Bu üründe hangi kumaş renkleri seçilebilir olsun?"}),
    )
    admin.site.register(Favorite)
@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ("title", "link_url", "order")

@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ("title", "badge_text", "order")
    list_editable = ("order",)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "rating", "is_approved", "created_at")
    list_filter = ("is_approved", "rating")
    list_editable = ("is_approved",)
    search_fields = ("product__name", "user__email", "comment")
    readonly_fields = ("product", "user", "rating", "comment", "created_at")   

