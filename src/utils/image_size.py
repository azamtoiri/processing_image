from io import BytesIO

from PIL import Image


def get_image_size(image_data) -> tuple:
    """
    Функция для получения размеров изображения.

    Аргументы:
    image_path (str): Путь к изображению.

    Возвращает:
    tuple: Кортеж из двух значений (ширина, высота) в пикселях.
    """
    with Image.open(BytesIO(image_data)) as img:
        width, height = img.size
        print("image original", width, height)
        return width, height


