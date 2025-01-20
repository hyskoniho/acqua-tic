import base64
from io import BytesIO
from PIL import Image

def base64_to_image(base64_string):
    """
    Converts a Base64 string to an image and returns it as a BytesIO object.
    
    :param base64_string: The Base64 string of the image.
    :return: The BytesIO object containing the image.
    """
    # Remove the prefix 'data:image/png;base64,' (if it exists)
    if base64_string.startswith('data:image'):
        base64_string = base64_string.split(',')[1]

    # Decode the base64 string
    image_data = base64.b64decode(base64_string)

    # Create an image from the binary data
    image = Image.open(BytesIO(image_data))

    # Create a BytesIO buffer to store the image
    img_io = BytesIO()
    image.save(img_io, 'PNG')
    img_io.seek(0)  # Return to the beginning of the buffer

    return img_io
