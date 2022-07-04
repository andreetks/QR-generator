import qrcode
from PIL import Image
import requests
import shutil
import os

QR_URL = ''
QR_NAME = ''
LOGO_PATH = ''
TYPE = 0
LOGO = ''

def menu():
    print('''
    MENU
1. Generate QR Code
2. Generate QR Code with image
3. Exit
''')

def request_data(type):
    global QR_URL, QR_NAME
    if type == 1:
        QR_URL = input('Enter the text to be encoded: ')
        QR_NAME = input('Enter de name of the final QR image: ')
    elif type == 2:
        QR_URL = input('Enter the text to be encoded: ')
        QR_NAME = input('Enter de name of the final QR image: ')


def request_image():
    global LOGO_PATH, LOGO
    LOGO_PATH = input('Enter the path to the logo(jpg/png): ')
    try:
        response = requests.get(LOGO_PATH, stream=True)
        if response.status_code == 200:
            with open('logo.jpg', 'wb') as image:
                shutil.copyfileobj(response.raw, image)
            try:
                LOGO = Image.open('logo.jpg')
                return False
            except:
                print('Error: The file is not an image')
                return True
        else:
            print('Error: The image is not found')
            return True
    except:
        print('Error: Invalid URL')
        return True


def generate_qr(type):
    if type == 1:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=3
        )
        qr.add_data(QR_URL)
        qr.make(fit=True)

        img = qr.make_image(fill_color='black', back_color='white')
        img.save(QR_NAME)
    elif type == 2:
        while True:
            if request_image():
                pass
            else:
                break

        logo = Image.open('logo.jpg')

        basewidht = 100

        wpercentage = (basewidht/float(logo.size[0]))
        hsize = int((float(logo.size[1])*float(wpercentage)))
        logo = logo.resize((basewidht,hsize), Image.ANTIALIAS)
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)

        qr.add_data(QR_URL)

        qr.make()

        Qrimg = qr.make_image(
            fill_color='black', back_color="white").convert('RGB')

        pos = ((Qrimg.size[0] - logo.size[0]) // 2,
            (Qrimg.size[1] - logo.size[1]) // 2)


        Qrimg.paste(logo, pos)

        Qrimg.save(QR_NAME)

        os.remove('logo.jpg')


if __name__ == '__main__':
    menu()
    TYPE = int(input())
    if TYPE == 3:
        exit(1)
    else:
        request_data(TYPE)
        generate_qr(TYPE)