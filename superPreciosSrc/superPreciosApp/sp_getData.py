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
    products = {product["name"]: product for product in entities["product"].values()}.values()
    return products

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
    products = {product["display_name"]: product for product in search_items}.values()
    return products

def getMercadonaData(term):
    page = 0
    market_uri = (
        "https://7uzjkl1dj0-dsn.algolia.net/1/indexes/products_prod_4315_es/query"
        "?x-algolia-application-id=7UZJKL1DJ0&x-algolia-api-key=9d8f2e39e90df472b4f2e559a116fe17"
    )
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
    products = {product["name"]: product for product in products_found}.values()
    print(products)
    return products
    
def getAldiData(term):
    market_uri = (
        "https://l9knu74io7-dsn.algolia.net/1/indexes/*/queries"
        "?X-Algolia-Api-Key=19b0e28f08344395447c7bdeea32da58"
        "&X-Algolia-Application-Id=L9KNU74IO7"
    )
    headers = {
        'Content-Type': 'application/json'
    }
    body = {
        "requests": [
            {
                "indexName": "prod_es_es_es_offers",
                "params": f"clickAnalytics=true&facets=[]&highlightPostTag=%3C%2Fais-highlight-0000000000%3E"
                          f"&highlightPreTag=%3Cais-highlight-0000000000%3E&hitsPerPage=12&page=0&query={term}"
                          "&tagFilters="
            },
            {
                "indexName": "prod_es_es_es_assortment",
                "params": f"clickAnalytics=true&facets=[]&highlightPostTag=%3C%2Fais-highlight-0000000000%3E"
                          f"&highlightPreTag=%3Cais-highlight-0000000000%3E&hitsPerPage=12&page=0&query={term}"
                          "&tagFilters="
            }
        ]
    }

    response = requests.post(market_uri, headers=headers, data=json.dumps(body))
    response_json = response.json()
    
    products = []
    results = response_json.get("results", [])
    for result in results:
        hits = result.get("hits", [])
        for product_json in hits:
            if product_json.get("salesPrice") is not None:
                product = {
                    "market": "ALDI",
                    "brand": "-",
                    "name": product_json.get("productName"),
                    "price": product_json.get("salesPrice"),
                    "image": product_json.get("productPicture") or ""
                }
                products.append(product)

    with open('productosAldi.txt', 'w') as f:
        for product in products:
            f.write(f"Nombre: {product['name']}\n")
            f.write(f"Precio: {product['price']} EUR\n")
            f.write(f"Imagen: {product['image']}\n\n")
            
    products = {product["name"]: product for product in products}.values()
    print("Datos guardados en productosAldi.txt")
    
    return products

def getConsumData(term):
    market_uri = f"https://tienda.consum.es/api/rest/V1.0/catalog/searcher/products?q={term}&limit=20&showRecommendations=false"
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.get(market_uri, headers=headers)
    response_json = response.json()
    
    products = []
    catalog = response_json.get("catalog", {})
    products_json_list = catalog.get("products", [])

    for product_json in products_json_list:
        product_data = product_json.get("productData", {})
        price_data = product_json.get("priceData", {})
        
        if product_data and price_data:
            product = {
                "market": "CONSUM",
                "brand": "-",
                "name": product_data.get("description", ""),
                "price": None,
                "price_unit": None,
                "image": None
            }
            
            # Precio
            prices = price_data.get("prices", [])
            if prices:
                prices_obj = prices[0].get("value", {})
                product["price"] = prices_obj.get("centAmount", 0) / 100  # Convertir centAmount a euros
                
                # Precio unitario
                cent_unit_amount = prices_obj.get("centUnitAmount")
                if cent_unit_amount:
                    unit_price_unit_type = price_data.get("unitPriceUnitType", "")
                    product["price_unit"] = f"{cent_unit_amount / 100} €/ {unit_price_unit_type}"

            # Imagen
            media = product_json.get("media", [])
            if media:
                product["image"] = media[0].get("url", "")

            products.append(product)

    with open('productosConsum.txt', 'w') as f:
        for product in products:
            f.write(f"Nombre: {product['name']}\n")
            f.write(f"Precio: {product['price']} EUR\n")
            if product['price_unit']:
                f.write(f"Precio por unidad: {product['price_unit']}\n")
            if product['image']:
                f.write(f"Imagen: {product['image']}\n")
            f.write("\n")

    print("Datos guardados en productosConsum.txt")
    products = {product["name"]: product for product in products}.values()
    return products


'''def get_carrefour_data(term):
    # Configura los parámetros de ScraperAPI y la URL de Carrefour
    payload = {
        'api_key': '2782e77d1b13c60075f96f6024a86741',
        'url': f'https://www.carrefour.es/search-api/query/v1/search?query={term}&scope=desktop&lang=es&rows=24&start=0&origin=default&f.op=OR'
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
        'Accept': 'application/json'
    }

    # Realiza la solicitud a ScraperAPI
    response = requests.get('https://api.scraperapi.com/', params=payload, headers=headers)
    
    # Verifica el código de respuesta
    if response.status_code == 200:
        try:
            data = response.json()
            # Procesa los productos
            products = data.get('content', {}).get('docs', [])
            with open('productosCarrefour.txt', 'w') as f:
                for product in products:
                    name = product.get("display_name", "Nombre no disponible")
                    price = product.get("active_price", "Precio no disponible")
                    image = product.get("image_path", "Imagen no disponible")
                    f.write(f"Nombre: {name}\n")
                    f.write(f"Precio: {price} EUR\n")
                    f.write(f"Imagen: {image}\n\n")
            print("Datos guardados en productosCarrefour.txt")
        except requests.exceptions.JSONDecodeError:
            print("Error: La respuesta no es un JSON válido")
    else:
        print("Error al obtener los datos:", response.status_code)
        print("Contenido de la respuesta:", response.text)
'''
