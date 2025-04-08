# Importing library
import sys
import qrcode
from PIL import Image


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('no argument')
        sys.exit()



    # Data to encode
    #data = "GeeksforGeeks11GeeksforGeeks12GeeksforGeeks13GeeksforGeeks14GeeksforGeeks15GeeksforGeeks16GeeksforGeeks17GeeksforGeeks18GeeksforGeeks19GeeksforGeeks20GeeksforGeeks21GeeksforGeeks22GeeksforGeeks23"
    data = sys.argv[1]
    print("QRcode Data String = %s" % data)

    filename = "default_QRcode.png"
    filename2 = "default_QRcode_81x81.png"
    if len(sys.argv) > 2:
        filename = sys.argv[2] + ".png"
        filename2 = sys.argv[2] + "_81x81.png"

    # Creating an instance of QRCode class
    qr = qrcode.QRCode(version = 1,
                       box_size = 2,
                       border = 1)

    # Adding data to the instance 'qr'
    qr.add_data(data)

    qr.make(fit = True)
    img = qr.make_image(fill_color = 'black',
                        back_color = 'white')

    img.save(filename)

    resize = (81, 81)
    img = img.resize(resize)
    img.save(filename2)

