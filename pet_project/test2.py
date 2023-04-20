import requests
from bs4 import BeautifulSoup

# List of car brands to search for
brands = ['Audi', 'BMW', 'Chevrolet', 'Ford', 'Honda', 'Hyundai', 'Kia', 'Lexus', 'Mazda', 'Mercedes-Benz', 'Nissan', 'Peugeot', 'Porsche', 'Renault', 'Skoda', 'Subaru', 'Suzuki', 'Tesla', 'Toyota', 'Volkswagen', 'Volvo']

for brand in brands:
    # Format the search URL with the brand name
    search_url = f'https://www.carlogos.org/car-logos/{brand.lower()}-logo.png'
    
    # Send a HEAD request to the https://www.carlogos.org/car-logos/toyota-logo.pngsearch URL to check if the logo file exists
    #response = requests.head(search_url)
    
    # Check if the logo file exists
    #if response.status_code == 200:
        #logo_url = search_url
    print(f'{brand}: {search_url}')
