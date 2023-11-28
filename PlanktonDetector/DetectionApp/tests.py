from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .forms import DetectForm
from django.conf import settings


# Test sprawdza czy wprowadzone pliki są w odpowiednim formacie
class CanUploadFiles(TestCase):
    def test_upload_img_file(self):
        file = SimpleUploadedFile(
            name="jpg_file.jpg",
            content=open(f"{settings.MEDIA_ROOT}/test_image.jpg", "rb").read(),
            content_type="image/jpg",
        )
        form = DetectForm(files={"image": file})
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_upload_other_file(self):
        file = SimpleUploadedFile(
            "txt_file.txt", content=b"some text", content_type="text/plain"
        )
        form = DetectForm(files={"image": file})
        self.assertFalse(form.is_valid())
