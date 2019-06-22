from oscar.apps.shipping import methods


class Reserve(methods.NoShippingRequired):
    code = 'RESERVE'
    name = 'Reserve'
    description = 'Items will be reserved at the warehouse for 7 days'
