from django.conf import settings
from PIL import Image, ImageDraw
import os
import requests
import base64

url = "https://detect.roboflow.com/plankton-vhsho/1"
api_key = os.environ["API_KEY_ROBO"]


def predict_image(image):
    with open(image.image.path, "rb") as f:
        enc_image = base64.b64encode(f.read())
    results = requests.post(
        url=url,
        params={"api_key": api_key},
        data=enc_image,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    for box in results.json()["predictions"]:
        save_image(box, image)

    return results.json()


def save_image(box, source_img):
    x1 = box["x"] - box["width"] / 2
    x2 = box["x"] + box["width"] / 2
    y1 = box["y"] - box["height"] / 2
    y2 = box["y"] + box["height"] / 2
    bounding_box = ((x1, y1), (x2, y2))
    class_ = box["class"]

    source = Image.open(source_img.image.path).convert("RGB")
    draw = ImageDraw.Draw(source)
    text_pos = (bounding_box[0][0] + 5, bounding_box[0][1] + 5)
    left, top, right, bottom = draw.textbbox(text_pos, class_, font_size=15)
    draw.rectangle((left, top - 4, right + 5, bottom + 5), fill="blue")
    draw.text(text_pos, class_, color="white", font_size=15)
    draw.rectangle(bounding_box, width=5, outline="blue")

    source.save(
        f"{settings.MEDIA_ROOT}/{source_img.image.name.split('.')[0]}_predicted.{source_img.image.name.split('.')[-1]}",
        "JPEG",
    )
