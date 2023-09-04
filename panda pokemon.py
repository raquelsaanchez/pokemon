import requests
import pandas as pd
from bs4 import BeautifulSoup

# Obtain API's information
def obtener_informacion_pokemon(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("No se pudo obtener la información del Pokémon.")
        return None

#Evolution
def obtener_informacion_evolucion(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_name}/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        evolution_chain_url = data['evolution_chain']['url']
        
        response = requests.get(evolution_chain_url)
        if response.status_code == 200:
            evolution_data = response.json()
            evolutions = []

            # Procesar la cadena de evolución
            while 'chain' in evolution_data:
                current_pokemon = evolution_data['chain']['species']['name']
                evolutions.append(current_pokemon.capitalize())
                evolution_data = evolution_data['chain']['evolves_to'][0] if evolution_data['chain']['evolves_to'] else {}
            
            return " -> ".join(evolutions) if evolutions else "N/A"
        else:
            print("No se pudo obtener la información de evolución del Pokémon.")
            return "N/A"
    else:
        print("No se pudo obtener la información de evolución del Pokémon.")
        return "N/A"
    
    
    #Double damage from
def obtener_double_damage_from(tipo):
    url = f"https://pokeapi.co/api/v2/type/{tipo}/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        double_damage_from = [entry['name'] for entry in data['damage_relations']['double_damage_from']]
        return ', '.join(double_damage_from) if double_damage_from else "N/A"
    else:
        print("No se pudo obtener la información de 'double damage from'.")
        return "N/A"

#Double damage to"
def obtener_double_damage_to(tipo):
    url = f"https://pokeapi.co/api/v2/type/{tipo}/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        double_damage_to = [entry['name'] for entry in data['damage_relations']['double_damage_to']]
        return ', '.join(double_damage_to) if double_damage_to else "N/A"
    else:
        print("No se pudo obtener la información de 'double damage to'.")
        return "N/A"

    
# HTML creation
def crear_html_pokemon(pokemon_info, evolucion_info, double_damage_from, double_damage_to, df_pokemon):
    tipo = pokemon_info['types'][0]['type']['name']
    fondo_color = ""
    letras_color = ""
    
    if tipo == "fire":
        fondo_color = "red"
        letras_color = "white"
    elif tipo == "water":
        fondo_color = "blue"
        letras_color = "white"
    elif tipo == "electric":
        fondo_color = "yellow"
        letras_color = "black"
    elif tipo == "grass":
        fondo_color = "green"
        letras_color = "black"
    
    html = f"""
    <html>
    <head>
        <title>Información de Pokémon</title>
    </head>
    <body style="background-color: {fondo_color}; color: {letras_color};">
        <h1>{pokemon_info['name'].capitalize()}</h1>
        <img src="{pokemon_info['sprites']['front_default']}" alt="{pokemon_info['name']}" style="max-width: 400px;">
        <h2>General Information:</h2>
        {df_pokemon.to_html()}
        <h2>Evolution:</h2>
        <p>Evolution from: {evolucion_info}</p>
        <h2>Double Damage From:</h2>
        <p>{double_damage_from}</p>
        <h2>Double Damage To:</h2>
        <p>{double_damage_to}</p>
        
    </body>
    </html>
    """
    
    with open(f"{pokemon_info['name'].lower()}.html", "w") as file:
        file.write(html)


#Menu
print("Elige un número:")
print("1. Charizard")
print("2. Bulbasaur")
print("3. Butterfree")
print("4. Wartortle")

numero_elegido = input("Ingresa el número correspondiente al Pokémon: ")

# Assign the chosen number to a pokemon
pokemon_mapping = {
    '1': 'charizard',
    '2': 'bulbasaur',
    '3': 'butterfree',
    '4': 'wartortle'
}

pokemon_name = pokemon_mapping.get(numero_elegido)

if pokemon_name:
    pokemon_info = obtener_informacion_pokemon(pokemon_name)
    evolucion_info = obtener_informacion_evolucion(pokemon_name)
    if pokemon_info:
        double_damage_from = obtener_double_damage_from(pokemon_info['types'][0]['type']['name'])
        double_damage_to = obtener_double_damage_to(pokemon_info['types'][0]['type']['name'])
        df_pokemon = pd.DataFrame({
            'Nombre': [pokemon_info['name'].capitalize()],
            'Tipo': [pokemon_info['types'][0]['type']['name'].capitalize()],
            'HP': [pokemon_info['stats'][0]['base_stat']],
            'Ataque': [pokemon_info['stats'][1]['base_stat']],
            'Defensa': [pokemon_info['stats'][2]['base_stat']],
            'Experiencia Base': [pokemon_info['base_experience']],
            'Habilidades': [", ".join([ability['ability']['name'].capitalize() for ability in pokemon_info['abilities']])]
        })
        crear_html_pokemon(pokemon_info, evolucion_info, double_damage_from, double_damage_to, df_pokemon)
        print(f"Se ha creado un archivo HTML para {pokemon_name.capitalize()}.")
else:
    print("Número no válido. Por favor, elige un número del 1 al 4.")