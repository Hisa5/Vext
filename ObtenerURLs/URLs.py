import requests
from bs4 import BeautifulSoup
import urllib.parse
import pandas as pd

def get_pdf_urls(base_url):
    def crawl(url):
        print(f"Accediendo a: {url}")  # Mostrar la URL que está siendo accedida
        # Realizar la solicitud al sitio web
        response = requests.get(url)
        response.raise_for_status()  # Asegura que la solicitud fue exitosa

        # Analizar el contenido HTML de la página
        soup = BeautifulSoup(response.content, 'html.parser')

        # Encontrar todos los enlaces en la página
        links = soup.find_all('a')

        for link in links:
            href = link.get('href')
            if href:
                full_url = urllib.parse.urljoin(url, href)
                if full_url.endswith('.pdf'):
                    print(f"Encontrado PDF: {full_url}")  # Mostrar URL del PDF encontrado
                    category, product, filename = extract_info(full_url)
                    pdf_urls.append({
                        'Categoría': category,
                        'Producto': product,
                        'Nombre del archivo': filename,
                        'URL': full_url
                    })
                elif full_url.endswith('/') and full_url.startswith(base_url):
                    if full_url not in visited:
                        visited.add(full_url)
                        crawl(full_url)

    pdf_urls = []
    visited = set()
    
    crawl(base_url)
    return pdf_urls

def extract_info(pdf_url):
    # Extraer información basada en la estructura de la URL
    parts = pdf_url.replace(base_url, '').strip('/').split('/')
    category = parts[0] if len(parts) > 0 else ''
    product = parts[1] if len(parts) > 1 else ''
    filename = parts[-1] if pdf_url.endswith('.pdf') else ''
    return category, product, filename

# URL base
base_url = 'https://terragene.com/wp-content/uploads/COA/'

# Obtener las URLs de los PDFs
pdf_urls = get_pdf_urls(base_url)

# Convertir la lista de URLs de PDFs a un DataFrame de pandas
df = pd.DataFrame(pdf_urls)

# Guardar el DataFrame en un archivo Excel
output_file = 'pdf_urls.xlsx'
df.to_excel(output_file, index=False)

print(f"\nArchivo Excel guardado como {output_file}")

# Mostrar las URLs de los PDFs
print("\nURLs de PDFs encontrados:")
for pdf in pdf_urls:
    print(pdf)
