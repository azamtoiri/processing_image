from io import BytesIO

from PIL import Image


def resize_image(image_data, size):
    with Image.open(BytesIO(image_data)) as img:
        img.thumbnail(size, Image.LANCZOS)
        buffer = BytesIO()
        img.save(buffer, format="JPEG")
        return buffer.getvalue()


def resize_image_2(image_data, size):
    with Image.open(image_data) as img:
        new_img = img.resize(size)
        new_img.save('new_image.jpg')
        # img.save(new_img)
        # img.thumbnail(size, Image.LANCZOS)
        # buffer = BytesIO()
        # img.save(buffer, format="JPEG")
        # return buffer.getvalue()


if __name__ == '__main__':
    result = resize_image_2('test_image.jpg', (150, 120))
    print(result)
