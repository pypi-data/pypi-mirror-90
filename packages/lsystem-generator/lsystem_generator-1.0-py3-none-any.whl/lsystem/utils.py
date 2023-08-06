import io
import numpy as np
import math
from PIL import Image

def plot2Image(plot):
    try:
        # save plt figure into a memory bytes buffer
        buf = io.BytesIO()
        plot.savefig(buf, format='png')
        #change stream position to the beginning
        buf.seek(0)
        #read buffer into PIL image
        im = Image.open(buf)
        return im
    except Exception as e:
        print(e)

