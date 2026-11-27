from decimal import Decimal

from django.test import TestCase
from rest_framework.test import APIClient

from .models import Category, Product


class CatalogApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name='Audio', description='Sonido y música')
        self.other_category = Category.objects.create(name='Video', description='Imagen')
        self.product = Product.objects.create(
            category=self.category, name='Auriculares', description='Bluetooth',
            price=Decimal('129.90'), stock=7,
        )

    def test_product_list_embeds_category_in_one_response(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, 200)
        item = response.data['results'][0]
        self.assertEqual(item['category']['name'], 'Audio')
        self.assertEqual(item['category']['description'], 'Sonido y música')

    def test_category_filter_returns_only_matching_products(self):
        Product.objects.create(category=self.other_category, name='Cámara', description='4K', price=500, stock=2)
        response = self.client.get(f'/api/products/?category={self.category.id}')
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], self.product.id)

    def test_product_create_accepts_category_id_and_returns_nested_category(self):
        response = self.client.post('/api/products/', {
            'name': 'Parlante', 'description': 'Portátil', 'price': '89.00',
            'stock': 3, 'category_id': self.category.id,
        }, format='multipart')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['category']['name'], 'Audio')

    def test_product_update_and_delete(self):
        response = self.client.patch(f'/api/products/{self.product.id}/', {'stock': 12}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['stock'], 12)
        response = self.client.delete(f'/api/products/{self.product.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Product.objects.filter(pk=self.product.id).exists())

    def test_product_rejects_negative_price(self):
        response = self.client.post('/api/products/', {
            'name': 'Invalido', 'description': 'Precio negativo', 'price': '-1.00',
            'stock': 1, 'category_id': self.category.id,
        }, format='multipart')
        self.assertEqual(response.status_code, 400)

    def test_category_crud_endpoint(self):
        response = self.client.post('/api/categories/', {'name': 'Accesorios', 'description': 'Varios'}, format='json')
        self.assertEqual(response.status_code, 201)
        category_id = response.data['id']
        response = self.client.patch(f'/api/categories/{category_id}/', {'name': 'Accesorios varios'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Accesorios varios')
