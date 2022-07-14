import code
from PIL import Image
from io import BytesIO
from codecs import encode
import base64


def open_image(input_string):
    print(BytesIO(base64.b64decode(input_string)).getvalue())
    im = Image.open(BytesIO(base64.b64decode(input_string)))
    im.show()


with open('sample_base64', ) as f:
    coded_string = f.read().replace('\n', '')
    coded_string +='==' # concatenate correct padding

img = '''R0lGODlhDwAPAKECAAAAzMzM/////wAAACwAAAAADwAPAAACIISPeQHsrZ5ModrLl
N48CXF8m2iQ3YmmKqVlRtW4MLwWACH+H09wdGltaXplZCBieSBVbGVhZCBTbWFydFNhdmVyIQAAOw==''' 

open_image(img)
open_image(coded_string)