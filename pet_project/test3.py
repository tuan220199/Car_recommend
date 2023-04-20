import requests
from bs4 import BeautifulSoup

url = "ttps://www.carlogos.org/car-logos/toyota-logo.png"

response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

first_image = soup.find("img")["src"]

print(first_image)