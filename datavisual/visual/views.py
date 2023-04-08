import matplotlib.pyplot as plt
import numpy as np
from django.shortcuts import render

#UploadCSV
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
import csv

###
import plotly.graph_objs as go
import io
import base64


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def visual(request):
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([3, 7, 2, 9, 5])
    fig, ax = plt.subplots()
    ax.scatter(x, y)
    ax.set_title("Scatter Plot")
    ax.set_xlabel("X Axis")
    ax.set_ylabel("Y Axis")
    plt.savefig("visual/static/scatterplot.png")
    return render(request, "visual/visual.html")

#visual/templates/

# def show_visualizations(request):
#     if request.method == 'POST':
#         filename = request.POST.get('filename')
#         fs = FileSystemStorage(LOCATION='visual/data/')
#         with fs.open(filename, 'r') as csvfile:
#             reader = csv.DictReader(csvfile)
#             data = [row for row in reader]

#         # create scatter plot
#         x_values = [float(row['x']) for row in data]
#         y_values = [float(row['y']) for row in data]
#         plt.scatter(x_values, y_values)
#         plt.xlabel('X')
#         plt.ylabel('Y')
#         scatter_plot = get_image()

#         # create bar chart
#         categories = [row['category'] for row in data]
#         counts = {}
#         for category in categories:
#             if category in counts:
#                 counts[category] += 1
#             else:
#                 counts[category] = 1
#         labels = list(counts.keys())
#         values = list(counts.values())
#         plt.bar(labels, values)
#         plt.xlabel('Category')
#         plt.ylabel('Count')
#         bar_chart = get_image()

#         # create heatmap
#         x_values = [float(row['x']) for row in data]
#         y_values = [float(row['y']) for row in data]
#         heatmap, xedges, yedges = np.histogram2d(x_values, y_values, bins=10)
#         extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
#         plt.clf()
#         plt.imshow(heatmap.T, extent=extent, origin='lower')
#         plt.xlabel('X')
#         plt.ylabel('Y')
#         heatmap_plot = get_image()

#         # create line plot
#         x_values = [row['timestamp'] for row in data]
#         y_values = [float(row['value']) for row in data]
#         plt.plot(x_values, y_values)
#         plt.xlabel('Timestamp')
#         plt.ylabel('Value')
#         line_plot = get_image()

#         # create box plot
#         data_values = [float(row['value']) for row in data]
#         plt.boxplot(data_values)
#         plt.ylabel('Value')
#         box_plot = get_image()

#         context = {
#             'scatter_plot': scatter_plot,
#             'bar_chart': bar_chart,
#             'heatmap_plot': heatmap_plot,
#             'line_plot': line_plot,
#             'box_plot': box_plot,
#             'data': data
#         }
#         return render(request, 'visualization.html', context)

#     return render(request, 'visual/results.html')


def get_image():
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.clf()
    image_base64 = base




def process_csv(file):
    decoded_file = file.read().decode('utf-8').splitlines()
    reader = csv.DictReader(decoded_file)
    data = []
    for row in reader:
        data.append(row)
    return data, reader.fieldnames

def upload_csv(request):
    if request.method == 'POST':
        file = request.FILES['csv_file']
        lo=file
        if not file.name.endswith('.csv'):
            messages.error(request, 'This is not a CSV file')
            return HttpResponseRedirect(reverse('upload'))
        

        data, headers = process_csv(file)

        #file_text = file.read().decode('utf-8').splitlines()

        fs = FileSystemStorage(location='visual/data/')
        filename = fs.save(file.name, file)
        uploaded_file_url = fs.url(filename)

        data = pd.read_csv(file)
        headers = list(data.columns)

        # Generate the visualizations
        line_plot = False
        bar_plot = False
        pie_chart = False
        scatter_plot = False
        if len(headers) >= 2:
            # Line Plot
            try:
                plt.plot(data[headers[0]], data[headers[1]])
                plt.xlabel(headers[0])
                plt.ylabel(headers[1])
                plt.title('Line Plot')
                plt.savefig('static/visual/line_plot.png')
                line_plot = True
            except:
                pass

            # Bar Plot
            try:
                plt.bar(data[headers[0]], data[headers[1]])
                plt.xlabel(headers[0])
                plt.ylabel(headers[1])
                plt.title('Bar Plot')
                plt.savefig('static/visual/bar_plot.png')
                bar_plot = True
            except:
                pass

            # Pie Chart
            try:
                plt.pie(data[headers[1]], labels=data[headers[0]])
                plt.title('Pie Chart')
                plt.savefig('static/visual/pie_chart.png')
                pie_chart = True
            except:
                pass

            # Scatter Plot
            try:
                sns.scatterplot(data=data, x=headers[0], y=headers[1])
                plt.title('Scatter Plot')
                plt.savefig('static/visual/scatter_plot.png')
                scatter_plot = True
            except:
                pass

        return render(request, 'visualization.html', {
            'uploaded_file_url': uploaded_file_url,
            'headers': headers,
            'line_plot': line_plot,
            'bar_plot': bar_plot,
            'pie_chart': pie_chart,
            'scatter_plot': scatter_plot
        })


       # return render(request, 'visual/results.html', {'data': data, 'headers': headers})

    return render(request, 'visual/upload.html')

# #upload as CSV
# def upload_csv(request):
#     if request.method == 'POST':
#         file = request.FILES['csv_file']
#         if not file.name.endswith('.csv'):
#             messages.error(request, 'This is not a CSV file')
#             return HttpResponseRedirect(reverse('upload'))
        
#         # Open the uploaded file in text mode
#         file_text = file.read().decode('utf-8').splitlines()

#         # fs = FileSystemStorage(location='visual/data/')
#         # filename = fs.save(file.name, file)
#         # uploaded_file_url = fs.url(filename)

#         # Process the CSV data here
#         # Read and process the CSV data
#         reader = csv.reader(file_text)
#         header_row = next(reader)
#         data = [[] for _ in header_row]
#         for row in reader:
#             for i, value in enumerate(row):
#                 data[i].append(value)

#         # Render a response to the user using a template that displays the processed data
#         context = {
#             'headers': header_row,
#             'data': data,
#         }
#         return render(request, 'visual/result.html', context)

#         #return HttpResponseRedirect(reverse('uploadcsv'))

#     return render(request, 'visual/upload.html')


# #Processing the CSV
# def process_csv(request):
#     # Assuming the CSV file has been uploaded and saved to the file system
#     with open('/path/to/uploaded/file.csv', 'r') as csvfile:
#         reader = csv.reader(csvfile)

#         # Extract the header row
#         header_row = next(reader)

#         # Create empty lists to hold the processed data
#         data = [[] for _ in header_row]

#         # Process each row of data
#         for row in reader:
#             # Add each element in the row to the appropriate list in the data array
#             for i, value in enumerate(row):
#                 data[i].append(value)

#     # Render a response to the user using a template that displays the processed data
#     context = {
#         'headers': header_row,
#         'data': data,
#     }
#     return render(request, 'results.html', context)

