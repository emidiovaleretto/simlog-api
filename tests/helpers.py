from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile


def create_test_image(width, height, fmt="PNG"):
    image = Image.new(mode="RGB", size=(width, height))
    buffer = BytesIO()
    image.save(buffer, format=fmt)

    return SimpleUploadedFile(
        name=f"test.{fmt.lower()}",
        content=buffer.getvalue(),
        content_type=f"image/{fmt.lower()}"
    )
