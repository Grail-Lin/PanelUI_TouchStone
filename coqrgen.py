
'''
launch program

inital qr code reader
	send 57 00 00 03 04 01 00 00 00 00 00 1F 71 50 41
    recv 31 00 00 03 04 01 00 00 00 00 00 FF F8 50 41

if error, exit

if ok, do while loop for trigger

'''

from pylibdmtx.pylibdmtx import encode
from PIL import Image

class COQRCodeGen:  # BT' baud = 9600
    def __init__(self):
        return

		
    def genImg(self, text, filename, height = 14.5, weight = 14.5):
        encoded = encode(text.encode('utf8'))
        img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
        img.save('%s.png' % filename)




if __name__ == "__main__":
    # test QRCodeReader
    qrgen = COQRCodeGen()
    qrgen.genImg("abcdefg-12345", "test")

