import json
import requests

api = 'https://tienda.mercadona.es/api/categories/'
api = requests.get(api)

# Sacar todas las categorias de la api
data = json.loads(api.text)
results = data['results']


with open('productosMercadona.txt', 'a') as f:
    idsCategories = []
    for result in results:
        for category in result['categories']:
            idsCategories.append(category['id'])

    # Sacar los productos de cada categoria
    for idCategory in idsCategories:
        urlCategories = 'https://tienda.mercadona.es/api/categories/' + str(idCategory)
        urlCategories = requests.get(urlCategories)
        data = json.loads(urlCategories.text)

        products = data['categories']
        for i in products:
            for product in i['products']:
                name = product['display_name']
                image = product['thumbnail']
                price = product['price_instructions']['reference_price']
                print(name, image)
                f.write("Nombre: " + name + '\n')
                f.write("Imagen: " + image + '\n')
                f.write("Precio: " + price + '\n')
                try:
                    price_discount = product['price_instructions']['previous_unit_price'].replace(' ', '')
                    f.write("Precio con descuento: " + price_discount + '\n')
                except:
                    pass
        print('\n\n\n')
