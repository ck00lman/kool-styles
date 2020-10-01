from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product

def favorites_contents(request):

    favorites_items = []
    favorites_total = 0
    product_count = 0
    favorites = request.session.get('favorites', {})

    for item_id, item_data in favorites.items():
        if isinstance(item_data, int):
            product = get_object_or_404(Product, pk=item_id)
            favorites_total += item_data * product.price
            product_count += item_data
            favorites_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
            })
        else:
            product = get_object_or_404(Product, pk=item_id)
            for size, quantity in item_data['items_by_size'].items():
                favorites_total += quantity * product.price
                product_count += quantity
                favorites_items.append({
                    'item_id': item_id,
                    'quantity': quantity,
                    'product': product,
                    'size': size,
                })

    if favorites_total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = favorites_total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - favorites_total
    else:
        delivery = 0
        free_delivery_delta = 0
    
    favorites_grand_total = delivery + total
    
    context = {
        'favorites_items': favorites_items,
        'favorites_total': favorites_total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'favorites_grand_total': favorites_grand_total,
    }

    return context