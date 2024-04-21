from pokemon import Pokemon
import requests
import re

input = "charizard" #input("Enter name of pokemon: ")
#input = "eevee"

pokemon_query = "https://pokeapi.co/api/v2/pokemon/"
pokemon_species_query = "https://pokeapi.co/api/v2/pokemon-species/"

pokemon_res = requests.get(pokemon_query + input)
pokemon_species_res = requests.get(pokemon_species_query + input)

if not pokemon_res.status_code:
    raise Exception(f"pokemon call failed with code: {pokemon_res.status_code}")

if not pokemon_species_res.status_code:
    raise Exception(f"pokemon Specie3s call failed with code: {pokemon_species_res.status_code}")

pokemon_data = pokemon_res.json()
pokemon_species_data = pokemon_species_res.json()
description = pokemon_species_data["flavor_text_entries"].pop(0)["flavor_text"]
description = re.subn('[\n\f]', ' ', description)[0]

pokemon = Pokemon(input, pokemon_data["types"], description)

print(pokemon.dex_entry())
