from io import BytesIO
from django.conf import settings
from PIL import Image, ImageDraw
import os
import requests
import base64
from ultralytics import YOLO
from PIL import Image, ImageDraw
from io import BytesIO
import os
from django.conf import settings
import cv2

# Załaduj lokalny model YOLOv8
model = YOLO("best.pt")

def predict_image(image):
    results = model.predict(source=image.image.path)
    img = results[0].plot()
    cv2.imwrite(
        f"{settings.MEDIA_ROOT}/{image.image.name.split('.')[0]}_predicted.{image.image.name.split('.')[-1]}",
        img,
    )
    predictions = []
    for result in results:
        
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            width = x2 - x1
            height = y2 - y1
            pred = {
                "x": x1,
                "y": y1,
                "width": width,
                "height": height,
                "class": result.names[int(box.cls[0])],  # nazwa klasy
                "confidence": float(box.conf[0])
            }
            predictions.append(pred)    
    predicitons = {"predictions": predictions}
    return predicitons

def save_image(box, source_img, len):
    pass


url = "https://detect.roboflow.com/plankton-vhsho/1"
api_key = f"{os.environ.get('RF_API_KEY')}"


# def predict_image(image):
#     with open(image.image.path, "rb") as f:
#         enc_image = base64.b64encode(f.read())
#     results = requests.post(
#         url=url,
#         params={"api_key": api_key},
#         data=enc_image,
#         headers={"Content-Type": "application/x-www-form-urlencoded"},
#     )
#     if results.json()["predictions"]:
#         save_image(
#             results.json()["predictions"], image, len(results.json()["predictions"])
#         )
#     return results.json()


# def save_image(box, source_img, len):
#     x = 0
#     with open(source_img.image.path, "rb") as fh:
#         bytes = BytesIO(fh.read())
#     source = Image.open(bytes).convert("RGB")
#     while x < len:
#         x1 = box[x]["x"] - box[x]["width"] / 2
#         x2 = box[x]["x"] + box[x]["width"] / 2
#         y1 = box[x]["y"] - box[x]["height"] / 2
#         y2 = box[x]["y"] + box[x]["height"] / 2
#         bounding_box = ((x1, y1), (x2, y2))
#         class_ = box[x]["class"]

#         draw = ImageDraw.Draw(source)
#         text_pos = (bounding_box[0][0] + 5, bounding_box[0][1] + 5)
#         left, top, right, bottom = draw.textbbox(text_pos, class_)
#         draw.rectangle((left, top - 4, right + 5, bottom + 5), fill="blue")
#         draw.text(text_pos, class_, color="white", font_size=30)
#         draw.rectangle(bounding_box, width=5, outline="blue")
#         x += 1

#     bytes.seek(0)
#     bytes.close()
#     source.save(
#         f"{settings.MEDIA_ROOT}/{source_img.image.name.split('.')[0]}_predicted.{source_img.image.name.split('.')[-1]}",
#         "JPEG",
#     )

