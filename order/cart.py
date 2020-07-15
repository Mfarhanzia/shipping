from decimal import Decimal
from django.conf import settings
from .models import ContainerPricing


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, quantity, furnished_option, product, price):
        product_id = str(product.id)
        # if product_id not in self.cart:
        self.cart[product_id] = {
            'model_image': product.model_image,
            'no_of_floors': product.no_of_floors,
            'variant': product.variant,
            'square_feet': product.square_feet,
            'quantity': quantity,
            'furnished_option': furnished_option,
            'price': price}
        # if update_quantity:
        #     self.cart[product_id]['quantity'] = quantity
        # else:
        #     self.cart[product_id]['quantity'] += quantity
        self.save()

    def add_custom(self, no_of_floors, cus_qty, width, depth, furnishing_option_custom, product, price):
        product_id = str(product.id)
        self.cart[product_id] = {
            'no_of_floors': no_of_floors,
            'quantity': cus_qty,
            'width': width,
            'depth': depth,
            'sqfeet_per_room': product.sqfeet_per_room,
            'furnishing_option_custom': furnishing_option_custom,
            'price': price
            }
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    # def __iter__(self):
    #     product_ids = self.cart.keys()
    #     products = ContainerPricing.objects.filter(id__in=product_ids)
    #     print("------")
    #     for product in products:
    #         a = self.cart[str(product.id)]['product'] = product
    #
    #     for item in self.cart.values():
    #         item['price'] = Decimal(item['price'])
    #         item['price'] = item['price']
    #         item['total_price'] = item['price'] * item['quantity']
    #         yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        total = 0
        for key in self.cart:
            data = self.cart[key]
            if "width" in data.keys():
                total += data["price"]
            else:
                total += (data['price'] * data['quantity'])
        return total

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
