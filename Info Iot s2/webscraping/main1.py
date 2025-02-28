import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

# url = input("Geef een URL: ")

# response = requests.get(url)
# if response.status_code != 200:
#     print("Er is een probleem met de website.")
#     print(f"Statuscode: {response.status_code}")
#     exit()

# soup = BeautifulSoup(response.text, "html.parser")

# # stockAmount = soup.find("p", class_="instock availability").text.strip()
# # print(f"er zijn {stockAmount} boeks in stock")

# # rating_Tag = soup.find("p", class_="star-rating")
# # rating = rating_Tag["class"][1]
# # print(f"{rating}")

# # description_tag  = soup.find("div", id="product_description")

# # if description_tag:
# #     description_text = description_tag.find_next("p").text.strip()
# #     print(f"beschrijving: {description_text}")
# # else:
# #     print("geen beschrijving gevonden.")

url = "https://pokemondb.net/pokedex/all"
response = requests.get(url)

if response.status_code != 200:
    print("Fout bij ophalen van de website")
    exit()

soup = BeautifulSoup(response.text, "html.parser")

table = soup.find("table", {"id": "pokedex"})

rows = table.find("tbody").find_all("tr")

pokemon_list = []

for row in rows:
    cols = row.find_all("td")
    num = cols[0].text.strip() # number van de pokemon
    naam = cols[1].text.strip()  # Naam van de Pokémon
    types = [t.text for t in cols[2].find_all("a")]  # Type(s)
    hp = int(cols[4].text.strip())

    pokemon_list.append(
        {
            "Number": num,
            "Naam": naam,
            "Types": ", ".join(types),
            "HP": hp,
        }
    )   
pokemon_list_sort_by_HP = sorted(pokemon_list, key=lambda pokemon: pokemon["HP"])

print(tabulate(pokemon_list_sort_by_HP,headers="keys",tablefmt="grid"))