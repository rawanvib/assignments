import pyqrcode

# string to represent qr code
img = 'simpleqr'

# generate qr code
url = pyqrcode.create(img)

# create and save svg file
url.svg('myqr.svg', scale=8)

# create and save the png file
url.png('myqr.png', scale=6)