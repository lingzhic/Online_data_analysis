import base64
import io
import math
import urllib

from collections import Counter
from matplotlib.pylab import *
import numpy as np
import pandas as pd


def get_graph():
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=600)
    buf.seek(0)
    image_png = buf.getvalue()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    buf.close()
    return graphic