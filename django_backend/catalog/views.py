from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Product


def serialize_product(product):
    return {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'stock': product.stock,
        'category': product.category.name if product.category else None,
        'image': product.image,
        'created_at': product.created_at.isoformat(),
    }


class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.order_by('name')
        return Response([{'id': item.id, 'name': item.name} for item in categories])


class ProductListView(APIView):
    def get(self, request):
        query = request.query_params.get('q', '').strip()
        category_id = request.query_params.get('category')
        sort_by = request.query_params.get('sort', 'newest')

        products = Product.objects.select_related('category')
        if query:
            products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
        if category_id and category_id.isdigit():
            products = products.filter(category_id=int(category_id))

        ordering = {'price_asc': 'price', 'price_desc': '-price'}.get(sort_by, '-created_at')
        return Response([serialize_product(product) for product in products.order_by(ordering)])


class ProductDetailView(APIView):
    def get(self, request, product_id):
        product = get_object_or_404(Product.objects.select_related('category'), pk=product_id)
        return Response(serialize_product(product))
