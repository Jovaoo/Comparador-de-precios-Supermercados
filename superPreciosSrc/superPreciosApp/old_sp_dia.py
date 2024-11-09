import requests
from bs4 import BeautifulSoup
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
}

urls = ['https://www.dia.es/navidad/c/L124','https://www.dia.es/charcuteria-y-quesos/c/L101','https://www.dia.es/carniceria/c/L102','https://www.dia.es/pescados-mariscos-y-ahumados/c/L103','https://www.dia.es/verduras/c/L104','https://www.dia.es/frutas/c/L105','https://www.dia.es/leche-huevos-y-mantequilla/c/L108','https://www.dia.es/yogures-y-postres/c/L113','https://www.dia.es/arroz-pastas-y-legumbres/c/L106','https://www.dia.es/aceites-salsas-y-especias/c/L107','https://www.dia.es/conservas-caldos-y-cremas/c/L114','https://www.dia.es/panes-harinas-y-masas/c/L112','https://www.dia.es/cafe-cacao-e-infusiones/c/L109','https://www.dia.es/azucar-chocolates-y-caramelos/c/L110','https://www.dia.es/galletas-bollos-y-cereales/c/L111','https://www.dia.es/patatas-fritas-encurtidos-y-frutos-secos/c/L115','https://www.dia.es/pizzas-y-platos-preparados/c/L116','https://www.dia.es/congelados/c/L119','https://www.dia.es/agua-refrescos-y-zumos/c/L117','https://www.dia.es/cervezas-vinos-y-bebidas-con-alcohol/c/L118','https://www.dia.es/limpieza-y-hogar/c/L122','https://www.dia.es/perfumeria-higiene-salud/c/L121','https://www.dia.es/bebe/c/L120','https://www.dia.es/mascotas/c/L123']
#charcuteria_y_quesos = requests.get("https://www.dia.es/charcuteria-y-quesos/c/L101", headers=headers)
#soup = BeautifulSoup(charcuteria_y_quesos.text, 'html.parser')
#ver_todos = soup.find_all('div', class_='basic-section-l1__view-category')


with open('productosDia.txt', 'a') as f:
    for url in urls:
        htmlPasillo = requests.get(url, headers=headers)
        soupPasillo = BeautifulSoup(htmlPasillo.text, 'html.parser')
        ver_todos = soupPasillo.find_all('div', class_='basic-section-l1__view-category')
        for i in ver_todos:
            # sacar el link de cada categoria
            link = i.find('a')['href']
            pag_siguiente = 1
            # variable para controlar el bucle
            control = True
            while control:

                categoria = requests.get('https://www.dia.es' + link, headers=headers)
                html = BeautifulSoup(categoria.text, 'html.parser')

                # comprobar que la pagina no sea la ultima
                print(link)
                pag_siguiente = (pag_siguiente + 1)
                if 'pag-' not in link:
                    link = link.replace('/c/', '/pag-' + str(pag_siguiente) + '/c/')
                else:
                    link = link.replace('/pag-' + str(pag_siguiente - 1) + '/', '/pag-' + str(pag_siguiente) + '/')

                # sacar los productos del script "<script defer type="application/ld+json">"
                script = html.find_all('script', type='application/ld+json')

                for s in script:
                    # Cargar el contenido del script como JSON
                    data = json.loads(s.string)
                    if data['itemListElement'] == []:
                        control = False
                        break
                    for item in data['itemListElement']:

                        product = item['item']
                        name = product['name']
                        image = product['image']

                        f.write("Nombre: " + name + '\n')
                        f.write("Imagen: " + image + '\n')
                        
                        try:
                            price = str(product['offers']['price'])
                            f.write("Precio: " + price + '\n')
                        except:
                            highPrice = str(product['offers']['highPrice'])
                            lowPrice = str(product['offers']['lowPrice'])
                            f.write("Precio sin oferta: " + highPrice + '\n')
                            f.write("Precio con oferta: " + lowPrice + '\n')




                    
            f.write('\n\n\n')


# https://www.dia.es/charcuteria-y-quesos/foie-pate-y-sobrasada/c/L2012
# https://www.dia.es/charcuteria-y-quesos/foie-pate-y-sobrasada/pag-2/c/L2012
