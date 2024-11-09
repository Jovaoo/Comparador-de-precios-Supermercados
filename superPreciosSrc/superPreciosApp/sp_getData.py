import json
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
}

def getAlcampoData(term):
    api_url = 'https://www.compraonline.alcampo.es/api/v5/products/search?limit=10000&offset=0&sort=name&term=' + term
    response = requests.get(api_url, headers=headers)
    data = response.json()

    entities = data['entities']

    with open('productosAlcampo.txt', 'w+') as f:
        for product_id, product_data in entities['product'].items():

            name = product_data.get("name")
            price = product_data.get("price", {}).get("current", {}).get("amount")
            image_src = product_data.get("image", {}).get("src")
            
            f.write(f"Nombre: {name}\n")
            f.write(f"Precio: {price}\n")
            f.write(f"Imagen: {image_src}\n\n")

        print("Datos guardados en productosAlcampo.txt")

def getDiaData(term):

    page = 1
    api_url = f'https://www.dia.es/api/v1/search-back/search/reduced?q={term}&page={page}'
    response = requests.get(api_url, headers=headers)
    data = response.json()


    search_items = data.get('search_items', [])
    image_base_url = "https://www.dia.es"

    with open('productosDia.txt', 'w') as f:
        while search_items != []:
            for item in search_items:

                name = item.get("display_name")
                price = item.get("prices", {}).get("price")
                image_src = image_base_url + item.get("image", "")

                f.write(f"Nombre: {name}\n")
                f.write(f"Precio: {price} EUR\n")
                f.write(f"Imagen: {image_src}\n\n")

            page += 1
            api_url = f'https://www.dia.es/api/v1/search-back/search/reduced?q={term}&page={page}'
            response = requests.get(api_url, headers=headers)
            data = response.json()
            search_items = data.get('search_items', [])

    print("Datos guardados en productosDia.txt")

def getMercadonaData(term):
    page = 0
    market_uri = (
        "https://7uzjkl1dj0-dsn.algolia.net/1/indexes/products_prod_4315_es/query"
        "?x-algolia-application-id=7UZJKL1DJ0&x-algolia-api-key=9d8f2e39e90df472b4f2e559a116fe17"
    )
    headers = {"Content-Type": "application/json"}
    products_found = []

    with open('productosMercadona.txt', 'w') as f:
        while True:
            # Crear payload de la solicitud, con la paginación en cada iteración
            payload = json.dumps({
                "params": f"query={term}&clickAnalytics=true&analyticsTags=%5B%22web%22%5D&getRankingInfo=true&page={page}"
            })
            
            # Hacer la solicitud POST
            response = requests.post(market_uri, headers=headers, data=payload)

            response_json = response.json()
            hits = response_json.get("hits", [])
            
            # Si no hay más resultados, salimos del bucle
            if not hits:
                break

            # Procesar cada producto en hits
            for product_json in hits:
                name = product_json.get("display_name", "")
                price = product_json.get("price_instructions", {}).get("unit_price", 0.0)
                image_src = product_json.get("thumbnail", "")

                # Formatear y escribir en el archivo
                f.write(f"Nombre: {name}\n")
                f.write(f"Precio: {price} EUR\n")
                f.write(f"Imagen: {image_src}\n\n")

                # Añadir a la lista de productos encontrados (si es necesario para otros usos)
                products_found.append({"name": name, "price": price, "image": image_src})

            # Incrementar página
            page += 1

    print("Datos guardados en productosMercadona.txt")

def getAldiData(term):
    page = 1
    api_url = f'https://www.aldi.es/api/search?query={term}&page={page}'
    response = requests.get(api_url, headers=headers)
    data = response.json()

    products = data.get('products', [])
    image_base_url = "https://www.aldi.es"

    with open('productosAldi.txt', 'w') as f:
        while products != []:
            for product in products:

                name = product.get("name")
                price = product.get("price")
                image_src = image_base_url + product.get("image")

                f.write(f"Nombre: {name}\n")
                f.write(f"Precio: {price} EUR\n")
                f.write(f"Imagen: {image_src}\n\n")

            page += 1
            api_url = f'https://www.aldi.es/api/search?query={term}&page={page}'
            response = requests.get(api_url, headers=headers)
            data = response.json()
            products = data.get('products', [])

    print("Datos guardados en productosAldi.txt")