from django.http import HttpResponse


def wishlist(buy_list):
    if buy_list:
        shopping_list = 'Cписок покупок:\n'
        for data in buy_list:
            name = data['name']
            total = data['total']
            measurement_unit = data['measurement_unit']
            shopping_list += (
                f'{name} - {total} {measurement_unit}\n'
            )
        return HttpResponse(shopping_list, content_type='text/plain')
    return HttpResponse('Список пуст')
