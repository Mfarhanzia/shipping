from decimal import Decimal
from django.conf import settings
from .models import ContainerPricing
import json

class OrderClass(object):
    """ This class is being used to save container orders to session"""
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart


    def add(self,product, quantity=1, delivery_date=None):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'floors': product.no_of_floors,'variant': product.variant, 'price': int(product.price),'price21':int(product.price21),'quantity': quantity, "delivery_date":json.dumps(delivery_date, indent=4, sort_keys=True, default=str)}
        # if update_quantity:
        #     self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] = quantity
            self.cart[product_id]['delivery_date'] = json.dumps(delivery_date, indent=4, sort_keys=True, default=str)
        self.cart[product_id]['delivery_date'].replace('"','')
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
        
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = ContainerPricing.objects.filter(id__in=product_ids)
        for product in products:
            a=self.cart[str(product.id)]['product'] = product
            
        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['price'] = item['price']
            if item['quantity'] > 20:
                item['price'] = Decimal(item['price21'])
                item['total_price'] = item['price'] * item['quantity']
            else:
                item['total_price'] = item['price'] * item['quantity']

            yield item

    # def __len__(self):
    #     return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
