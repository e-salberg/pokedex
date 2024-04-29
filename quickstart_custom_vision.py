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

def add_images(pokemon, tag, general_tag, trainer, project, base_image_location):
    print("Adding images for {}...".format(pokemon))
    image_list = []

    for image_num in range(0, 41):
        file_name = "{0}_{1}.jpg".format(pokemon, image_num)
        with open(os.path.join(base_image_location, "training", pokemon, file_name), "rb") as image_contents:
            image_list.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(), tag_ids=[tag.id, general_tag.id]))

    upload_result = trainer.create_images_from_files(project.id, ImageFileCreateBatch(images=image_list))
    if not upload_result.is_batch_successful:
        print("Image batch upload failed.")
        for image in upload_result.images:
            print("Image status: ", image.status)
        exit(-1)

def test_prediction(test_pokemon, predictor, project, base_image_location):
    # Now there is a trained endpoint that can be used to make a prediction
    print("testing {}".format(test_pokemon))

    with open(os.path.join(base_image_location, "training", "test", "{}.jpg".format(test_pokemon)), "rb") as image_contents:
        results = predictor.classify_image(
            project.id, "classifyModel", image_contents.read())

        # Display the results.
        for prediction in results.predictions:
            print("\t" + prediction.tag_name +
                  ": {0:.2f}%".format(prediction.probability * 100))

def main():
    credentials = ApiKeyCredentials(in_headers={"Training-key": VISION_TRAINING_KEY})
    trainer = CustomVisionTrainingClient(VISION_TRAINING_ENDPOINT, credentials)
    prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": VISION_PREDICTION_KEY})
    predictor = CustomVisionPredictionClient(VISION_PREDICTION_ENDPOINT, prediction_credentials)

    #print(VISION_PREDICTION_RESOURCE_ID)
    #print(VISION_PREDICTION_ENDPOINT)
    #print(VISION_PREDICTION_KEY)

    publish_iteration_name = "classifyModel"
    credentials = ApiKeyCredentials(in_headers={"Training-key": VISION_TRAINING_KEY})
    trainer = CustomVisionTrainingClient(VISION_TRAINING_ENDPOINT, credentials)

    # Create a new project
    print ("Creating project...")
    project_name = "pokedex_vision" #uuid.uuid4()
    project = trainer.create_project(project_name)

    # Make two tags in the new project
    charizard_tag = trainer.create_tag(project.id, "Charizard")
    lugia_tag = trainer.create_tag(project.id, "Lugia")
    charmander_tag = trainer.create_tag(project.id, "Charmander")
    pokemon_tag = trainer.create_tag(project.id, "Pokemon")

    base_image_location = os.path.join (os.path.dirname(__file__), "images")

    add_images("charizard", charizard_tag, pokemon_tag, trainer, project, base_image_location)
    add_images("charmander", charmander_tag, pokemon_tag, trainer, project, base_image_location)
    add_images("lugia", lugia_tag, pokemon_tag, trainer, project, base_image_location)

    print("Training...")
    iteration = trainer.train_project(project.id)
    while(iteration.status != "Completed"):
        iteration = trainer.get_iteration(project.id, iteration.id)
        print("Training status: " + iteration.status)
        print("Waiting 10 seconds...")
        time.sleep(10)

    # The iteration is now trained. Publish it to the project endpoint
    trainer.publish_iteration(project.id, iteration.id, publish_iteration_name, VISION_PREDICTION_RESOURCE_ID)
    print ("Done!")

    test_prediction("charmander", predictor, project, base_image_location)
    test_prediction("charizard", predictor, project, base_image_location)
    test_prediction("lugia", predictor, project, base_image_location)
    
if __name__ == "__main__":
    main()