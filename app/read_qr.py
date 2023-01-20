from pdf2image.pdf2image import convert_from_bytes
from pyzbar.pyzbar import decode


async def read_qr(file):

    file_img = convert_from_bytes(file)
    data = decode(file_img[0])
   
    try:          
        url = str(data[0].data, encoding='utf-8')
        if url.startswith('https://cvcovid.salud.gob.mx/compruebaVacuna'):
            print('[INFO] QR is valid')
            return url
        else:
            print('[ERROR] QR is not valid')
            return None
    except Exception as e:
        print(e)
        print('[ERROR] Could not read QR')
        return None