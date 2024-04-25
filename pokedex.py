from pokemon import Pokemon
from google.cloud import texttospeech
import requests
import re

## tts - https://cloud.google.com/text-to-speech/docs/libraries
## need to pay :(

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

tts_client = texttospeech.TextToSpeechClient()
synthesis_input = texttospeech.SynthesisInput(text=pokemon.dex_entry())
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)

audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

response = tts_client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
)

with open("output.mp3", "wb") as out:
    out.write(response.audio_content)
    print("wrote audio file")