import requests

# Stuur een GET-verzoek naar de Joke API
response = requests.get('https://official-joke-api.appspot.com/random_joke')
json_response = response.json()

# Haal de grap en de punchline op uit de JSON-respons
setup = json_response['setup']
punchline = json_response['punchline']

# Print de grap
print(f'Joke: {setup}')
input("Press Enter to see the punchline...")
print(f'Punchline: {punchline}')