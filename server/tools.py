import base64
from io import BytesIO
from PIL import Image

def base64_to_image(base64_string):
    """
    Converte uma string Base64 para uma imagem e retorna como um objeto BytesIO.
    
    :param base64_string: A string Base64 da imagem.
    :return: O objeto BytesIO que contém a imagem.
    """
    # Remover o prefixo 'data:image/png;base64,' (caso exista)
    if base64_string.startswith('data:image'):
        base64_string = base64_string.split(',')[1]

    # Decodificar a string base64
    image_data = base64.b64decode(base64_string)

    # Criar uma imagem a partir dos dados binários
    image = Image.open(BytesIO(image_data))

    # Criar um buffer BytesIO para armazenar a imagem
    img_io = BytesIO()
    image.save(img_io, 'PNG')
    img_io.seek(0)  # Voltar ao início do buffer

    return img_io
