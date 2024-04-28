from pokemon import Pokemon
import requests
import re
import os
import azure.cognitiveservices.speech as speechsdk

input = "charizard" #input("Enter name of pokemon: ")
#input = "eevee"

pokemon_query = "https://pokeapi.co/api/v2/pokemon/"
pokemon_species_query = "https://pokeapi.co/api/v2/pokemon-species/"

# setting up tts
speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('AZURE_SPEECH_KEY'), region=os.environ.get('AZURE_SPEECH_REGION'))
audio_config =  speechsdk.audio.AudioOutputConfig(use_default_speaker=True) #speechsdk.audio.PullAudioOutputStream() # speechsdk.audio.AudioConfig(use_default_speaker=True)
speech_config.speech_synthesis_voice_name = 'en-US-AvaMultilingualNeural'
speech_sythesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

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
text = pokemon.dex_entry()

speech_result = speech_sythesizer.speak_text_async(text).get()

if speech_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print("Speech synthesized for text [{}]".format(text))