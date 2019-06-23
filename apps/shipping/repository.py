# from decimal import Decimal as D

# from oscar.apps.shipping.methods import FixedPrice, NoShippingRequired
# from oscar.apps.shipping.repository import Repository as CoreRepository

# # Dummy shipping methods
# method1 = FixedPrice(charge_excl_tax=D('10.00'), charge_incl_tax=D('10.00'))
# method1.code = 'method1'
# method1.description = 'Ship by van'

# method2 = FixedPrice(charge_excl_tax=D('20.00'), charge_incl_tax=D('20.00'))
# method2.code = 'method2'
# method2.description = 'Ship by boat'


# class Repository(CoreRepository):
#     methods = (method1, method2,)

from decimal import Decimal as D
from oscar.apps.shipping.methods import Free, FixedPrice, NoShippingRequired
from oscar.apps.shipping.repository import Repository as CoreRepository
from oscar.apps.shipping import methods, models
from oscar.apps.shipping.models import WeightBased
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

# hand delivery, eg for customers located near company premises
class HandDelivery(methods.NoShippingRequired):
    code = "hand-delivery"
    name = _("Hand Delivery")
    description = _("No shipping required. Product will be delivered hand to hand.")
    charge_excl_tax = D('00.00')

class Repository(CoreRepository):
    methods = [HandDelivery()]

    def get_available_shipping_methods(self, basket, user=None, shipping_addr=None,request=None, **kwargs):
        if shipping_addr:
            weightbased_set = WeightBased.objects.all().filter(
                countries=shipping_addr.country.code)
            if weightbased_set:
                methods = (list(weightbased_set))
                # methods += [HandDelivery()]
            else:
                methods = []
        else:
            # methods = [HandDelivery()]
            methods = []
        return methods
