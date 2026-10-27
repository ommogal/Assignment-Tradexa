from django.test import TestCase

from .services import ValidationError, recommend_box


def product(name="P", length=10, width=10, height=10, weight=1):
    return {
        "name": name,
        "length": length,
        "width": width,
        "height": height,
        "weight": weight,
    }


def box(name="B", length=20, width=20, height=20, max_weight=10, cost=50):
    return {
        "name": name,
        "length": length,
        "width": width,
        "height": height,
        "max_weight": max_weight,
        "cost": cost,
    }


class RecommendationTests(TestCase):
    def test_single_product_fits(self):
        result = recommend_box([product()], [box()])
        self.assertEqual(result["selected_box"]["name"], "B")

    def test_rotation_is_supported(self):
        p = product(length=12, width=8, height=5)
        b = box(length=10, width=8, height=12)
        result = recommend_box([p], [b])
        self.assertEqual(result["selected_box"]["name"], "B")

    def test_dimension_failure(self):
        p = product(length=30, width=30, height=30)
        self.assertIsNone(recommend_box([p], [box()]))

    def test_weight_failure(self):
        p = product(weight=11)
        self.assertIsNone(recommend_box([p], [box(max_weight=10)]))

    def test_cheapest_valid_box_selected(self):
        p = product()
        expensive = box(name="Expensive", cost=100)
        cheap = box(name="Cheap", cost=40)
        result = recommend_box([p], [expensive, cheap])
        self.assertEqual(result["selected_box"]["name"], "Cheap")

    def test_equal_cost_prefers_lower_unused_volume(self):
        p = product(length=10, width=10, height=10)
        small = box(name="Small", length=12, width=12, height=12, cost=50)
        large = box(name="Large", length=20, width=20, height=20, cost=50)
        result = recommend_box([p], [large, small])
        self.assertEqual(result["selected_box"]["name"], "Small")

    def test_multiple_products(self):
        products = [
            product(name="A", length=10, width=10, height=5),
            product(name="B", length=10, width=10, height=5),
        ]
        result = recommend_box(products, [box(length=20, width=10, height=10)])
        self.assertIsNotNone(result)

    def test_empty_products_rejected(self):
        with self.assertRaises(ValidationError):
            recommend_box([], [box()])

    def test_negative_dimension_rejected(self):
        with self.assertRaises(ValidationError):
            recommend_box([product(length=-1)], [box()])

    def test_http_endpoint(self):
        response = self.client.post(
            "/api/recommend/",
            data={
                "products": [product()],
                "boxes": [box()],
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["selected_box"]["name"], "B")
