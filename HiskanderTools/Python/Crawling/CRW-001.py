"""
Ruta de Ejecución:
   cd HiskanderTools/Python/Crawling
   python CRW-001.py
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import tldextract

# Módodulo para encontrar enlaces en sitios y cadena de caracteres
def find_links_on_page(url, target_domain, search_strings, current_depth, max_depth):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        matching_links = []

        page_text = soup.get_text()  # Obtener el contenido de la página como texto

        for link in soup.find_all('a'):
            href = link.get('href')
            if href:
                absolute_url = urljoin(url, href)
                parsed_url = urlparse(absolute_url)
                # Verificar si el dominio extraído contiene target_domain
                if target_domain in parsed_url.netloc:
                    matching_links.append(absolute_url)

        for search_string in search_strings:
            if search_string.lower() in page_text.lower():
                print(f'Se encontró "{search_string}" en {url}')
        
        return matching_links, len(matching_links)
    except Exception as e:
        print(f"Error al acceder a {url}: {e}")
        return [], 0
## Módodulo para encontrar enlaces en sitios y cadena de caracteres


## Módulo para Rastrear Sitio y encontrar enlaces.
def crawl_website_recursive(url, target_domain, search_strings, max_depth, current_depth=1):
    if current_depth > max_depth:
        return []

    visited_urls = set()
    to_visit = [(url, current_depth)]  # Usar una tupla para almacenar la URL y su profundidad
    matching_links = []

    while to_visit:
        url, current_depth = to_visit.pop()
        visited_urls.add(url)

        links_on_page, num_links = find_links_on_page(url, target_domain, search_strings, current_depth, max_depth)
        matching_links.extend(links_on_page)

        print(f"Nivel de profundidad {current_depth}: Número de enlaces en {url}: {num_links}")

        for link in links_on_page:
            if link not in visited_urls and current_depth < max_depth:
                to_visit.append((link, current_depth + 1))  # Incrementar la profundidad

    return matching_links
## Módulo para Rastrear Sitio y encontrar enlaces.

# Programa Principal
if __name__ == "__main__":
    start_url = "https://www.eada.edu"  # Cambia esto al sitio web que desees rastrear
    extracted = tldextract.extract(start_url)
    target_domain = f"{extracted.domain}.{extracted.suffix}"
    
    # Lista de cadenas de búsqueda
    search_strings = [
        "CIF",
        "C.I.F.",
        "Código de Identificación Fiscal"
        ]  
    
    max_depth = 5  # Cambia esto al nivel máximo de profundidad que desees
    
    # Print Operativo
    print('Inicio a:',target_domain)
    
    matching_links = crawl_website_recursive(start_url, target_domain, search_strings, max_depth)

    # Print Operativo
    print('matching links Culminado:')
    
    if matching_links:
        print("Enlaces asociados al dominio:")
        for link in matching_links:
            print(link)
    else:
        print("No se encontraron enlaces asociados al dominio.")

# Programa Principal
# More
