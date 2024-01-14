from django.conf import settings
from roboflow import Roboflow
import os

rf = Roboflow(api_key=os.environ["API_KEY_ROBO"])
model = rf.workspace().project("plankton-vhsho").version(1).model


def predict_image(image):
    results = model.predict(image.image.path)
    results.save(
        f"{settings.MEDIA_ROOT}/{image.image.name.split('.')[0]}_predicted.{image.image.name.split('.')[-1]}"
    )
    return results.json()
