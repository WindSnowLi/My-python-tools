# PIL :  pip3/pip install pillow
from PIL import Image

img = Image.open('./square-logo.png')
img.save('./square-logo.ico')