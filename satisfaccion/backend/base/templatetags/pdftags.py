from django import template

register = template.Library()


@register.filter
def percentage(value):
    try:
        valor = '{0:.2%}'.format(value)
        return valor.replace(",", "c").replace(".", ",").replace("c", ".")
    except:
        if value:
            return value
        else:
            return ""


# @register.filter
# def two_decimal(value):
#     try:
#         valor = '{:.2f}'.format(value)
#         return valor.replace(",", "c").replace(".", ",").replace("c", ".")
#     except:
#         if value:
#             return value
#         else:
#             return ""


# @register.filter
# def removeNan(value):
#     try:
#         if value == 'Nan':
#             return ""
#     except:
#         pass
#     return value
