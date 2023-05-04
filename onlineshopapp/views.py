from django.shortcuts import render
from .models import *
# Create your views here.

# Создаем функцию представления каталога
def show_catalog(request):
    #Создаем context в котором по ключю products храниться список обектов
    context = {"products":Product.objects.all()}
    # Создаем переменную в которой храниться страница
    response = render(request, 'catalog.html',context)
    # Если пользователь отправил запрос 
    if request.method == 'POST':
        # Получает по нужному имени из формы
        item_pk = request.POST.get("product_pk")
        item_count = request.POST.get("count")

        # Если в куках нет ключа products
        if "products" not in request.COOKIES:
            # Создаем ключ products значением которого являеться номер обекта и его количество
            response.set_cookie("products",str(item_pk)+" "+str(item_count))
        # Иначе
        else:
            # Создаем флаг совпадения
            flag_same_pk = False
            #Разделяем куки ключа products по знаку "|" и получаем список
            list_products = request.COOKIES['products'].split("|")
            #перебираем список
            for product in list_products:
                #Розбиваем строку в которой храниться номер обекта и его количество и получаем номер обекта который сравиваем с полученым номером
                if product.split(" ")[0] == str(item_pk):
                    #Совпадение произошло
                    flag_same_pk = True
                    #Создаем перекменную count в которой храниться сума полученого количества обектов и количество которое было у етого обекта до изменения
                    count = int(product.split(" ")[1]) + int(item_count)
                    #Создаем переменную new_product в которой мы создаем строку в которой храниться номер обекта и его новое количество
                    new_product = product.split(" ")[0] + " " + str(count)
                    #В списке с продуктами(номером и количеством) по нужному индексу заменяем значение
                    list_products[list_products.index(product)] = new_product
                    # Создаем переменную строки в которой храниться список представленный как строка вместо запятых в котором символ "|"
                    new_products = '|'.join(list_products)
                    break
            #Если не совпало
            if not flag_same_pk:
                #Создаем переменную в которой к старым кукам через "|" добавляем новые куки(номер и количество)
                new_products = request.COOKIES['products'] + "|" + str(item_pk)+" "+str(item_count)
            #Задаем куки 
            response.set_cookie('products',new_products)
    # Возвращаем пользователю страницу
    return response

# Создаем функцию представления корзины
def show_cart(request):
    # Если в куках есть ключ products
    if "products" in request.COOKIES:
        #Разделяем куки ключа products по знаку "|" и получаем список
        products_pk = request.COOKIES['products'].split("|")
        #Создаем список
        list_products = list() 
        #Перебераем список куков
        for product_pk in products_pk:
            #Создаем список в котором храниться обекст и его количество 
            list_object_and_count = [Product.objects.get(pk=product_pk.split(" ")[0]),product_pk.split(" ")[1]]
            # Добавляем етот список в общий список всех таких обектов
            list_products.append(list_object_and_count) 
        # Создаем переменную в которой храниться страница и в context передаем список всех обектов и количеств
        response = render(request,"cart.html",context={"products": list_products})
    #Если нет такого ключа
    else:
        # Создаем переменную в которой храниться страница и в context не передаем ничего
        response = render(request,"cart.html",context={"products":list()})
    # Если пользователь отправил запрос 
    if request.method == 'POST':
        # Получает данные по нужному имени из формы
        pk_product = request.POST.get("product_pk")
        count_product = request.POST.get("count") #  "Количество: 5"
        #Перезапизаписываем переменную и оставляем все что просле пробела
        count_product = int(count_product.split(" ")[-1])
        #Разделяем куки ключа products по знаку "|" и получаем список
        list_products = request.COOKIES['products'].split("|")
        #перебираем список
        for product in list_products:
            #Розбиваем строку в которой храниться номер обекта и его количество и получаем номер обекта который сравиваем с полученым номером
            if product.split(" ")[0] == str(pk_product):
                #Если количество продукта меньше или равно 0
                if count_product <= 0:
                    #Из списка с номерами и количеством продукта удаляем етот(на котором было совпадение) продукт
                    list_products.pop(list_products.index(product)) 
                    # Создаем переменную строки в которой храниться список представленный как строка вместо запятых в котором символ "|"
                    new_products = '|'.join(list_products)
                    # Если длина списка больше 0
                    if len(list_products) > 0:
                        #Перезадаем куки
                        response.set_cookie('products',new_products)
                    #Если список пустой
                    else:
                        #Удаляем куки по ключю products
                        response.delete_cookie('products')
                        
                #Если количество продукта больше 0
                else:
                    #Создаем переменную в которой храниться номер продукта и его количество
                    new_product = product.split(" ")[0] + " " + str(count_product)
                    #В списке с продуктами(номером и количеством) по нужному индексу заменяем значение
                    list_products[list_products.index(product)] = new_product
                    # Создаем переменную строки в которой храниться список представленный как строка вместо запятых в котором символ "|"
                    new_products = '|'.join(list_products)
                    #Задаем куки 
                    response.set_cookie('products',new_products)
                break

    
    # Возвращаем пользователю страницу
    return response 