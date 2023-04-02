import matplotlib.pyplot as plt
import numpy as np
from django.shortcuts import render

def visual(request):
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([3, 7, 2, 9, 5])
    fig, ax = plt.subplots()
    ax.scatter(x, y)
    ax.set_title("Scatter Plot")
    ax.set_xlabel("X Axis")
    ax.set_ylabel("Y Axis")
    plt.savefig("visual/static/scatterplot.png")
    return render(request, "visual.html")