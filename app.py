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
    bitmap: str  # Changed from List[int] to str
    width: int
    height: int


def get_image_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return Image.open(BytesIO(response.content))


def convert_to_monochrome(image, width=None, height=None):
    if width and height:
        image = image.resize((width, height), Image.Resampling.LANCZOS)
    bw_image = image.convert("1")  # 1-bit pixels, black and white
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
            bit = 0 if pixel else 1  # 0 is white, 1 is black
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
    # Format the bitmap as a C-style array string
    hex_values = [f"0x{byte:02x}" for byte in bitmap]
    return "{" + ", ".join(hex_values) + "}"


@app.post("/convert", response_model=BitmapResponse)
async def convert_image(request: ImageRequest):
    try:
        img = get_image_from_url(str(request.url))
        bw_img = convert_to_monochrome(img, request.width, request.height)
        bitmap = image_to_bitmap_array(bw_img)

        # Format the bitmap as a C-style array string
        formatted_bitmap = format_bitmap_as_c_array(bitmap)

        return BitmapResponse(
            bitmap=formatted_bitmap, width=request.width, height=request.height
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
