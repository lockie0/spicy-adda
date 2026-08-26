import unittest

from app import create_app
from app.models import Product
from app.utils import get_product_ingredients


class IngredientFeatureTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_challapunukulu_has_specific_ingredients(self):
        product = Product.query.filter_by(name='Challapunukulu').first()
        self.assertIsNotNone(product)
        ingredients = get_product_ingredients(product)
        self.assertIsInstance(ingredients, list)
        self.assertIn('Maida / All-Purpose Flour', ingredients)
        self.assertNotIn('Brown Sugar', ingredients)

    def test_combo_items_include_separate_ingredient_groups(self):
        product = Product.query.filter_by(name='Family Combo').first()
        self.assertIsNotNone(product)
        ingredients = get_product_ingredients(product)
        self.assertIsInstance(ingredients, dict)
        self.assertIn('included_items', ingredients)
        self.assertIn('Mirchi Bajji', ingredients['ingredient_groups'])

    def test_product_detail_page_displays_ingredients_section(self):
        product = Product.query.filter_by(name='Mirchi Bajji').first()
        self.assertIsNotNone(product)
        with self.app.test_client() as client:
            response = client.get(f'/product/{product.id}')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'INGREDIENTS', response.data)
            self.assertIn(b'Mirchi Bajji', response.data)


if __name__ == '__main__':
    unittest.main()
