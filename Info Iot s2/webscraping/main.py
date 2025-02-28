import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

url = "https://vincentpeters.github.io/scrape-table/"
response = requests.get(url)

if response.status_code != 200:
    print("Fout bij ophalen van de website")
    exit()

soup = BeautifulSoup(response.text, "html.parser")

table = soup.find("table")

rows = table.find("tbody").find_all("tr")

countrys = []

for row in rows:
    cols = row.find_all("td")
    stad = cols[0].text.strip() 
    land = cols[1].text.strip()  
    inwoners = int(cols[4].text.strip())
    groote = int(cols[5].text.strip())

    countrys.append(
        {
            "stad": f'{stad} ({land})',
            "inwoners": inwoners,
            "groote in km": groote,
        }
    )   
countrys_sort_by_area = sorted(countrys, key=lambda area: area["groote in km"], reverse=True)

print(tabulate(countrys_sort_by_area,headers="keys",tablefmt="grid"))