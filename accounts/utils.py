from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


def resize_image(picture_profile):
    base_width = 400
    image = Image.open(picture_profile)
    width = base_width / float(image.size[0])
    height = int(float(image.size[1]) * float(width))
    image = image.resize((base_width, height), Image.Resampling.LANCZOS)
    return image


def convert_type_image(image, filename):
    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    django_file = ContentFile(buffer.getvalue(), name=f"{filename}.jpg")
    return django_file
