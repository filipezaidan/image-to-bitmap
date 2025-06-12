# 🖼️ Image to Bitmap Converter API

A simple FastAPI service that fetches an image from a URL, resizes it to 128x64 (or custom size), converts it to monochrome (1-bit black & white), and returns the image data as a C-style bitmap array.

---

## 🚀 Features

* Fetch image from a URL.
* Resize and center it on a black canvas.
* Convert to monochrome (threshold-based).
* Return a C-compatible bitmap array.
* Customizable image size (default: 128x64).

---

## 📦 Requirements

* Python 3.8+
* [FastAPI](https://fastapi.tiangolo.com/)
* [Uvicorn](https://www.uvicorn.org/)
* [Requests](https://docs.python-requests.org/)
* [Pillow](https://pillow.readthedocs.io/)
* [Pydantic](https://docs.pydantic.dev/)

Install dependencies:

```bash
pip install -r requirements.txt
```

**`requirements.txt`**

```txt
fastapi==0.95.2
uvicorn==0.22.0
requests==2.31.0
Pillow==10.1.0
pydantic==1.10.7
```

---

## ▶️ Running the Server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at: [http://localhost:8000](http://localhost:8000)

Swagger docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📤 API Endpoint

### `POST /convert`

Convert an image from a given URL to a monochrome bitmap.

#### Request Body

```json
{
  "url": "https://example.com/image.png",
  "width": 128,
  "height": 64
}
```

* `url` (string, required): Direct link to the image.
* `width` (integer, optional): Desired image width (default: 128).
* `height` (integer, optional): Desired image height (default: 64).

#### Response

```json
{
  "bitmap": "{0xff, 0x81, 0x81, ...}",
  "width": 128,
  "height": 64
}
```

---

## 🧪 Example (using `curl`)

```bash
curl -X POST http://localhost:8000/convert \
  -H "Content-Type: application/json" \
  -d '{
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/PNG_transparency_demonstration_1.png/240px-PNG_transparency_demonstration_1.png",
        "width": 128,
        "height": 64
      }'
```

---

## 🛠️ Project Structure

```
├── main.py              # FastAPI app and logic
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

---

## 📄 License

This project is licensed under the MIT License.

---

Let me know if you want a version in Portuguese or want to include Docker support.
