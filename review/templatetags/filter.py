from django import template
register = template.Library()

@register.filter
def make_string(order_id, product_id):
    #noi chuoi
    return f"{product_id}_{order_id}"
@register.simple_tag
def check_reviewed(reviewed_product_ids, product_id, order_id):
    key = f"{product_id}_{order_id}"
    return key in reviewed_product_ids