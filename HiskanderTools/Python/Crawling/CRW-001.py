"""
Ruta de Ejecución:
cd HiskanderTools/Python/Crawling 
python CRW-001.py
python CRW-001.py
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import tldextract
import re

# Módulo para encontrar enlaces en sitios y cadena de caracteres
def find_links_on_page(url, target_domain, search_strings, current_depth, max_depth, verified_matches, max_requests):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        matching_links = []

        for search_string in search_strings:
            excluded_words = ["cifra", "cifras", "CIFRAS", "cifrado"]  # Agrega aquí las palabras que no deben considerarse coincidencias

            page_text = soup.get_text()  # Obtener el contenido de la página como texto
            index = page_text.lower().find(search_string.lower())
            if index != -1:
                start_index = max(0, index - 20)  # Comenzar 20 caracteres antes de la coincidencia
                end_index = min(len(page_text), index + len(search_string) + 20)  # Terminar 20 caracteres después de la coincidencia
                context_text = page_text[start_index:end_index]

                # Verificar si la coincidencia no es una palabra excluida
                is_excluded = any(excluded_word in context_text.lower() for excluded_word in excluded_words)
                if not is_excluded:
                    # Evaluar la coincidencia y contarla si cumple con un patrón
                    is_match, match_value = evaluate_match(search_string, context_text)
                    if is_match:
                        verified_matches += 1
                        print(f'{start_url} Encontrado "{search_string}" en {url} y coincidencia: "{match_value}". Coincidencia Nro {verified_matches}')

        for link in soup.find_all('a'):
            href = link.get('href')
            if href:
                absolute_url = urljoin(url, href)
                parsed_url = urlparse(absolute_url)
                # Verificar si el dominio extraído contiene target_domain
                if target_domain in parsed_url.netloc:
                    matching_links.append(absolute_url)

        return matching_links, len(matching_links), verified_matches
    except Exception as e:
        print(f"Error al acceder a {url}: {e}")
        return [], 0, verified_matches

# Evaluar coincidencia buscando patrones similares


def evaluate_match(search_string, context_text):
    # Expresión regular para verificar el formato de un CIF español
    cif_pattern = r'[ABCDEFGHJKLMNPQRSUVW]{1}\d{7}[0-9A-J]{1}'

    # Buscar coincidencias que cumplan con el formato de CIF
    cif_matches = re.search(cif_pattern, context_text, re.IGNORECASE)
    
    # Verificar si se encontraron coincidencias y si alguna coincide con el formato de CIF
    if cif_matches:
        match_value = cif_matches.group(0)
        print("Si es cif")
        return True, match_value  # Se encontró al menos una coincidencia de CIF
    else:
        return False, None  # No se encontraron coincidencias de CIF


# Módulo para Rastrear Sitio y encontrar enlaces.
def crawl_website_recursive(url, target_domain, search_strings, max_depth, current_depth=1, max_requests=35):
    print("me ejecuto Linea crawl_website_recursive")
    if current_depth > max_depth:
        return []

    visited_urls = set()
    to_visit = [(url, current_depth)]  # Usar una tupla para almacenar la URL y su profundidad
    matching_links = []
    verified_matches = 0
    request_counter = 0

    while to_visit and (verified_matches < 2 or verified_matches > 3) and request_counter <= max_requests:
        url, current_depth = to_visit.pop()
        visited_urls.add(url)

        links_on_page, num_links, verified_matches = find_links_on_page(url, target_domain, search_strings, current_depth, max_depth, verified_matches, max_requests)
        matching_links.extend(links_on_page)

        #print(f"Nivel de profundidad {current_depth}: Número de enlaces en {url}: {num_links}")
        print("Request ",request_counter)
        for link in links_on_page:
            if link not in visited_urls and current_depth < max_depth:
                to_visit.append((link, current_depth + 1))  # Incrementar la profundidad

        request_counter += 1

    return matching_links,verified_matches

# Programa Principal: Recorre todos los enlaces de la página a analizar y extrae todos los textos que contengan los search_strings.
if __name__ == "__main__":
    # TODO: Agregar un mecanismo que lea varías enlaces y que luego aplique la función.
    # Cambia esto al sitio web que desees rastrear
    start_url = "http://www.fcbarcelona.com"  
    
    # Extrae el dominio del sitio web
    extracted = tldextract.extract(start_url)
    target_domain = f"{extracted.domain}.{extracted.suffix}"
    
    # Lista de cadenas (strings) a buscar en los enlaces
    search_strings = [
        "CIF",
        "C.I.F.",
        "Código de Identificación Fiscal"
    ]

    max_depth = 5  # Cambia esto al nivel máximo de profundidad que desees
    
    # Print Operativo
    print('Inicio Crawling:', target_domain)
    
    matching_links = crawl_website_recursive(start_url, target_domain, search_strings, max_depth)

    # Print Operativo
    print(f'matching links Culminado: {len(matching_links)}')
    
    if matching_links:
        print("Enlaces asociados al dominio:")
        #for link in matching_links:
        #    print(link)
    else:
        print("No se encontraron enlaces asociados al dominio.")


# Programa Principal


#Prueba

#Prueba