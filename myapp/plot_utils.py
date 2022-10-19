import math
import base64
import io
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def get_graph():
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150)
    buf.seek(0)
    image_png = buf.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buf.close()
    return graph
