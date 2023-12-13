import json
from django.core.files import File
from PIL import Image
from io import BytesIO
from django.conf import settings
from ultralytics import YOLO

MODEL = YOLO("best.pt")


def predict_image(image):
    results = MODEL.predict(
        image.image.path,
        save=True,
        project=settings.MEDIA_ROOT,
        name=f"{image.image.name}_predicted",
        imgsz=[640, 640],
    )
    x = json.loads(results[0].tojson())
    return x
