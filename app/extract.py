import pdfplumber

async def extract_info (file):
    pdf = pdfplumber.open(file)
    page = pdf.pages[0]
    text = page.extract_text()
    try:
        text = text.split('\n')
        data = {'CURP': text[5], 'Nombre': text[8], 
        'Primera Dosis': {'Fecha': text[13].split(' ')[0], 'Marca': text[16].split(' ')[0], 
        'Lote': text[19].split(' ')[0]}, 'Segunda Dosis': {'Fecha': text[13].split(' ')[1], 
        'Marca': text[16].split(' ')[1], 'Lote': text[19].split(' ')[1]}}

        print('[INFO] extracted info from pdf')
        return data
    except Exception as e:
                print(e)
                print('[ERROR] Could not read PDF')
                return None
    

async def validate_certificate (curp_pdf, curp_ssalud):
    if curp_pdf == curp_ssalud:
        return True
    else:
        return False
