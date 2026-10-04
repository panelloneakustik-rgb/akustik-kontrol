from decimal import Decimal

from django.test import TestCase
from rest_framework.test import APIClient

from products.models import Category, Product, ProductVariant


class ProductVariantApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="Süngerler", slug="sungerler")
        self.product = Product.objects.create(
            category=self.category,
            name="Piramit Sünger",
            slug="piramit-sunger",
            price=Decimal("100"),
            stock=0,
        )
        self.v40 = ProductVariant.objects.create(
            product=self.product,
            thickness="40 mm",
            dimensions="100x100 cm",
            price=Decimal("850"),
            stock=10,
            order=0,
        )
        self.v20 = ProductVariant.objects.create(
            product=self.product,
            thickness="20 mm",
            dimensions="100x100 cm",
            price=Decimal("500"),
            stock=4,
            order=1,
        )

    def test_detail_lists_variants_on_one_product(self):
        res = self.client.get("/api/products/piramit-sunger/")
        self.assertEqual(res.status_code, 200)
        labels = [v["label"] for v in res.data["variants"]]
        self.assertEqual(len(labels), 2)
        self.assertTrue(any("40 mm" in x for x in labels))
        self.assertTrue(any("20 mm" in x for x in labels))

    def test_list_option_count(self):
        res = self.client.get("/api/products/")
        row = next(p for p in res.data["results"] if p["slug"] == "piramit-sunger")
        self.assertEqual(row["option_count"], 2)

    def test_cart_uses_selected_variant_price_and_stock(self):
        add = self.client.post(
            "/api/cart/aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee/add/",
            {"product": self.product.id, "variant": self.v20.id, "quantity": 1},
            format="json",
        )
        self.assertEqual(add.status_code, 201)
        item = add.data["items"][0]
        self.assertEqual(item["variant"], self.v20.id)
        self.assertEqual(Decimal(item["unit_price"]), Decimal("500.00"))
        self.assertIn("20 mm", item["variant_note"])

        over = self.client.post(
            "/api/cart/aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee/add/",
            {"product": self.product.id, "variant": self.v20.id, "quantity": 4},
            format="json",
        )
        self.assertEqual(over.status_code, 400)

    def test_public_stock_only_shown_when_five_or_fewer_remain(self):
        res = self.client.get("/api/products/piramit-sunger/")
        self.assertEqual(res.status_code, 200)
        by_thickness = {v["thickness"]: v["stock"] for v in res.data["variants"]}
        self.assertIsNone(by_thickness["40 mm"])
        self.assertEqual(by_thickness["20 mm"], 4)
        self.assertIsNone(res.data["stock"])

        listing = self.client.get("/api/products/")
        row = next(p for p in listing.data["results"] if p["slug"] == "piramit-sunger")
        self.assertIsNone(row["stock"])

        self.v40.stock = 0
        self.v40.save()
        self.v20.stock = 0
        self.v20.save()
        empty = self.client.get("/api/products/piramit-sunger/")
        self.assertEqual(empty.data["stock"], 0)
        self.assertTrue(all(v["stock"] == 0 for v in empty.data["variants"]))

    def test_add_requires_variant_when_several_exist(self):
        res = self.client.post(
            "/api/cart/bbbbbbbb-bbbb-4ccc-8ddd-eeeeeeeeeeee/add/",
            {"product": self.product.id, "quantity": 1},
            format="json",
        )
        self.assertEqual(res.status_code, 400)


class ProductAdminAddTests(TestCase):
    def setUp(self):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        self.user = User.objects.create_superuser("admin", "a@b.com", "pass")
        self.cat = Category.objects.create(name="Süngerler", slug="sungerler-2")
        self.client.force_login(self.user)

    def test_add_product_without_filling_empty_variant_row(self):
        url = "/admin/products/product/add/"
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        data = {
            "category": self.cat.pk,
            "name": "Yeni Panel",
            "slug": "yeni-panel",
            "price": "250.00",
            "discount_percent": "0",
            "stock": "3",
            "shipping_days": "2-4",
            "is_new": "on",
            "variants-TOTAL_FORMS": "1",
            "variants-INITIAL_FORMS": "0",
            "variants-MIN_NUM_FORMS": "0",
            "variants-MAX_NUM_FORMS": "1000",
            "variants-0-thickness": "",
            "variants-0-dimensions": "",
            "variants-0-density": "",
            "variants-0-color": "",
            "variants-0-price": "",
            "variants-0-discount_percent": "0",
            "variants-0-stock": "0",
            "variants-0-order": "0",
            "gallery_images-TOTAL_FORMS": "1",
            "gallery_images-INITIAL_FORMS": "0",
            "gallery_images-MIN_NUM_FORMS": "0",
            "gallery_images-MAX_NUM_FORMS": "1000",
            "gallery_images-0-image": "",
            "gallery_images-0-order": "0",
        }
        res = self.client.post(url, data, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(Product.objects.filter(slug="yeni-panel").exists())
        product = Product.objects.get(slug="yeni-panel")
        self.assertEqual(product.variants.count(), 1)
        self.assertEqual(product.variants.first().price, Decimal("250.00"))

