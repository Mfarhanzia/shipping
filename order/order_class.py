from decimal import Decimal
from django.conf import settings
from .models import ContainerPricing

class OrderClass(object):
    """ This class is being used to save container orders to session"""
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart


    def add(self,product, quantity=1):
        try:
            product_id = str(product.id)
            if product_id not in self.cart:
                self.cart[product_id] = {'floors': product.no_of_floors,'variant': product.variant, 'price': int(product.price),'quantity': quantity}
            # if update_quantity:
            #     self.cart[product_id]['quantity'] = quantity
            else:
                self.cart[product_id]['quantity'] = quantity
            
            self.save()
            print(";;;;;;;;;;;;;;;;")
        except Exception as e:
            print("00000000",e)
    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
        

    # def remove(self, product):
    #     product_id = str(product.id)
    #     if product_id in self.cart:
    #         del self.cart[product_id]
    #         self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = ContainerPricing.objects.filter(id__in=product_ids)
        print("------")
        for product in products:
            a=self.cart[str(product.id)]['product'] = product
            
        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['price'] = item['price']
            item['total_price'] = item['price'] * item['quantity']
            yield item

    # def __len__(self):
    #     return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())


    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
