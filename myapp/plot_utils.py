import math
import base64
import io
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime


def get_graph():
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150)
    buf.seek(0)
    image_png = buf.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buf.close()
    return graph


def get_time_interval(time_col):
    s1 = time_col[0]
    s2 = time_col[1]
    before = datetime.strptime(s1, '%H:%M:%S')
    after = datetime.strptime(s2, '%H:%M:%S')
    delta_t = after.timestamp() - before.timestamp()
    return int(delta_t)


def add_labels(x, y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha='center')
