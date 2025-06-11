from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import List
import requests
from io import BytesIO
from PIL import Image

app = FastAPI(title="Image to Bitmap Converter API")


class ImageRequest(BaseModel):
    url: HttpUrl
    width: int = 128
    height: int = 64


class BitmapResponse(BaseModel):
    bitmap: str
    width: int
    height: int


def get_image_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return Image.open(BytesIO(response.content))


def prepare_canvas_with_image(image, width, height, bg_color=(0, 0, 0)):
    # Redimensiona a imagem para ocupar todo o espaço disponível
    image = image.convert("RGBA")
    resized_img = image.resize((width, height), Image.Resampling.LANCZOS)

    # Cria fundo preto
    canvas = Image.new("RGBA", (width, height), bg_color + (255,))

    # Cola a imagem redimensionada
    canvas.paste(resized_img, (0, 0), resized_img)
    return canvas.convert("RGB")


def convert_to_monochrome(image, threshold=128):
    # Converte para escala de cinza
    gray_image = image.convert("L")
    # Aplica threshold (sem dithering)
    bw_image = gray_image.point(lambda x: 255 if x > threshold else 0, "1")
    return bw_image


def image_to_bitmap_array(image):
    pixels = image.load()
    width, height = image.size
    bitmap = []

    for y in range(height):
        byte = 0
        bit_count = 0
        for x in range(width):
            pixel = pixels[x, y]
            bit = 1 if pixel > 0 else 0  # 1 é branco, 0 é preto
            byte = (byte << 1) | bit
            bit_count += 1
            if bit_count == 8:
                bitmap.append(byte)
                byte = 0
                bit_count = 0
        if bit_count > 0:
            byte <<= 8 - bit_count
            bitmap.append(byte)

    return bitmap


def format_bitmap_as_c_array(bitmap):
    hex_values = [f"0x{byte:02x}" for byte in bitmap]
    return "{" + ", ".join(hex_values) + "}"


@app.post("/convert", response_model=BitmapResponse)
async def convert_image(request: ImageRequest):
    try:
        img = get_image_from_url(str(request.url))
        # Prepara canvas com fundo preto e imagem centralizada
        canvas = prepare_canvas_with_image(
            img, request.width, request.height, bg_color=(0, 0, 0)
        )
        # Converte para monocromático (sem dithering, threshold 128)
        bw_img = convert_to_monochrome(canvas, threshold=128)
        bitmap = image_to_bitmap_array(bw_img)
        formatted_bitmap = format_bitmap_as_c_array(bitmap)
        return BitmapResponse(
            bitmap=formatted_bitmap, width=request.width, height=request.height
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
