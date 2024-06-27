from io import BytesIO

from PIL import Image


def resize_image(image_data, size):
    with Image.open(BytesIO(image_data)) as img:
        img.thumbnail(size, Image.ANTIALIAS)
        buffer = BytesIO()
        img.save(buffer, format="JPEG")
        return buffer.getvalue()
