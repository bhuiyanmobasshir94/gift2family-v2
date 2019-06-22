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


from . import methods
from oscar.core.loading import get_model
from oscar.apps.shipping import repository

WeightBased = get_model('shipping', 'WeightBased')


class Repository(repository.Repository):
    def get_available_shipping_methods(self, basket, user=None,
                                       shipping_addr=None, request=None, **kwargs):

        if shipping_addr:
            weightbased_set = WeightBased.objects.all()

            if weightbased_set:
                return (list(weightbased_set), )

        # If no address was specified, or weight-based options are
        # not available, return the "Reserve" shipping option
        return (methods.Reserve(), )
