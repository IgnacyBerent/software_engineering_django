import json
from django.forms import ValidationError
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from .models import Product
from decimal import Decimal


@csrf_exempt
def product_list(request):
    if request.method == "GET":
        products = list(Product.objects.values("id", "name", "price", "available"))
        return JsonResponse(products, safe=False)
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON")

        name = data.get("name")
        price = data.get("price")
        available = data.get("available")

        if any([field is None for field in [name, price, available]]):
            return HttpResponseBadRequest("Missing required fields")

        try:
            product = Product(name=name, price=Decimal(str(price)), available=available)
            product.full_clean()
            product.save()
        except ValidationError as e:
            return HttpResponseBadRequest(f"Invalid data: {e}")

        return JsonResponse(
            {
                "id": product.id,
                "name": product.name,
                "price": float(product.price),
                "available": product.available,
            },
            status=201,
        )
    else:
        return HttpResponseNotFound("Unsupported HTTP method")


@csrf_exempt
def product_detail(request, product_id):
    if request.method == "GET":
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return HttpResponseNotFound("Product not found")
        return JsonResponse(
            {
                "id": product.id,
                "name": product.name,
                "price": float(product.price),
                "available": product.available,
            }
        )
    else:
        return HttpResponseNotFound("Unsupported HTTP method")
