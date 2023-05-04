from django.shortcuts import render
from .models import *
# Create your views here.

def show_catalog(request):
    context = {"products":Product.objects.all()}
    response = render(request, 'catalog.html',context)
    if request.method == 'POST':
        item_pk = request.POST.get("product_pk")
        item_count = request.POST.get("count")
        if "products" not in request.COOKIES:
            response.set_cookie("products",str(item_pk)+" "+str(item_count))
        else: 
            flag_same_pk = False
            list_products = request.COOKIES['products'].split("|")
            for product in list_products:
                if product.split(" ")[0] == str(item_pk):
                    flag_same_pk = True
                    count = int(product.split(" ")[1]) + int(item_count)
                    new_product = product.split(" ")[0] + " " + str(count)
                    list_products[list_products.index(product)] = new_product
                    new_products = '|'.join(list_products)
                    break
            if not flag_same_pk:
                new_products = request.COOKIES['products'] + "|" + str(item_pk)+" "+str(item_count)
                
            response.set_cookie('products',new_products)
    return response

def show_cart(request):
    if "products" in request.COOKIES:
        products_pk = request.COOKIES['products'].split('|')

        list_products = list() 

        for product_pk in products_pk:
            list_products.append([Product.objects.get(pk=product_pk.split(" ")[0]),product_pk.split(" ")[1]]) 
        print(list_products)
        response = render(request,"cart.html",context={"products": list_products})
    else:
        response = render(request,"cart.html",context={"products":list()})
    if request.method == 'POST':
        pk_product = request.POST.get("product_pk")
        count_product = request.POST.get("count")
        count_product = int(count_product.split(" ")[-1])
        list_products = request.COOKIES['products'].split("|")
        for product in list_products:
            if product.split(" ")[0] == str(pk_product):
                if count_product <= 0:
                    list_products.pop(list_products.index(product)) 
                    new_products = '|'.join(list_products)
                    if len(list_products) > 0:
                        response.set_cookie('products',new_products)
                    else:
                        response.delete_cookie('products')
                        
                    
                else:
                    new_product = product.split(" ")[0] + " " + str(count_product)
                    list_products[list_products.index(product)] = new_product
                    new_products = '|'.join(list_products)
                    response.set_cookie('products',new_products)
                break

    
    
    return response 