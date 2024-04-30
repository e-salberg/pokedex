from pokemon import Pokemon
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
import azure.cognitiveservices.speech as speechsdk
import os
import requests
import re


def main():
    SPEECH_KEY = os.environ.get('POKEDEX_SPEECH_KEY')
    SPEECH_REGION = os.environ.get('POKEDEX_SPEECH_REGION')
    VISION_PREDICTION_ENDPOINT = os.environ.get('POKEDEX_VISION_PREDICTION_ENDPOINT')
    VISION_PREDICTION_KEY = os.environ.get('POKEDEX_VISION_PREDICTION_KEY')
    VISION_TRAINING_ENDPOINT = os.environ.get('POKEDEX_VISION_TRAINING_ENDPOINT')
    VISION_TRAINING_KEY = os.environ.get('POKEDEX_VISION_TRAINING_KEY')


    credentials = ApiKeyCredentials(in_headers={"Training-key": VISION_TRAINING_KEY})
    trainer = CustomVisionTrainingClient(VISION_TRAINING_ENDPOINT, credentials)
    prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": VISION_PREDICTION_KEY})
    predictor = CustomVisionPredictionClient(VISION_PREDICTION_ENDPOINT, prediction_credentials)
    base_image_location = os.path.join (os.path.dirname(__file__), "images")
    project = trainer.get_projects()[0]
    publish_iteration_name = "classifyModel"

    with open(os.path.join(base_image_location, "training", "test", "charizard_shinny.jpg"), "rb") as image_contents:
        results = predictor.classify_image(
            project.id, publish_iteration_name, image_contents.read())

    input = results.predictions[1].tag_name.lower()
    print(input)
    #input = "charizard" #input("Enter name of pokemon: ")
    #input = "eevee"

    pokemon_query = "https://pokeapi.co/api/v2/pokemon/"
    pokemon_species_query = "https://pokeapi.co/api/v2/pokemon-species/"

    # setting up tts
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    audio_config =  speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    speech_config.speech_synthesis_voice_name = 'en-US-AvaMultilingualNeural'
    speech_sythesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    pokemon_res = requests.get(pokemon_query + input)
    pokemon_species_res = requests.get(pokemon_species_query + input)

    if not pokemon_res.status_code:
        raise Exception(f"pokemon call failed with code: {pokemon_res.status_code}")

    if not pokemon_species_res.status_code:
        raise Exception(f"pokemon Species call failed with code: {pokemon_species_res.status_code}")

    pokemon_data = pokemon_res.json()
    pokemon_species_data = pokemon_species_res.json()
    description = pokemon_species_data["flavor_text_entries"].pop(0)["flavor_text"]
    description = re.subn('[\n\f]', ' ', description)[0]
    
    pokemon = Pokemon(input, pokemon_data["types"], description)
    text = pokemon.dex_entry()

    speech_result = speech_sythesizer.speak_text_async(text).get()

    if speech_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(text))


if __name__ == "__main__":
    main()