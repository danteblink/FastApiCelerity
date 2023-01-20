from fastapi import FastAPI
from fastapi import UploadFile, File, Form, HTTPException
from read_qr import read_qr
from extract import extract_info, validate_certificate
from celery_worker import create_order

app = FastAPI()

@app.get("/")
async def root():
    return{"message": "Hola Mundo"}

@app.post("/uploads/")

async def receive_file(file: UploadFile = File(...), name: str = Form(...), birthDate: str = Form(...)):

    content = file.file.read()
    url = await read_qr(content)
    data_pdf = await extract_info(file.file)

    if url and data_pdf is not None:

        create_order.delay(name, url)

        return 'El archivo se subio correctamente. Se encuentra en proceso de validación.'

    else:
        return 'El archivo no es legible. Por favor intentelo de nuevo.'


