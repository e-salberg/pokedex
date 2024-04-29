from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import os, time, uuid

# git bash adds C:/Program Files/Git to env variables whose value starts with "/" this is my workaroud since I use git bash
# https://github.com/microsoft/vscode-python/issues/7104
VISION_PREDICTION_RESOURCE_ID = "/" + os.environ.get('POKEDEX_PREDICTION_RESOURCE_ID')
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

print("testing charmander")

with open(os.path.join(base_image_location, "training", "test", "charizard_shinny.jpg"), "rb") as image_contents:
    results = predictor.classify_image(
        project.id, publish_iteration_name, image_contents.read())

    # Display the results.
    for prediction in results.predictions:
        print("\t" + prediction.tag_name +
                ": {0:.2f}%".format(prediction.probability * 100))
"""

print("testing charizard")

with open(os.path.join(base_image_location, "training", "test", "charizard.jpg"), "rb") as image_contents:
    results = predictor.classify_image(
        project.id, publish_iteration_name, image_contents.read())

    # Display the results.
    for prediction in results.predictions:
        print("\t" + prediction.tag_name +
                ": {0:.2f}%".format(prediction.probability * 100))
        

print("testing lugia")

with open(os.path.join(base_image_location, "training", "test", "lugia.jpg"), "rb") as image_contents:
    results = predictor.classify_image(
        project.id, publish_iteration_name, image_contents.read())

    # Display the results.
    for prediction in results.predictions:
        print("\t" + prediction.tag_name +
                ": {0:.2f}%".format(prediction.probability * 100))
    
"""