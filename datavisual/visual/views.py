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

def show_visualization(request):
    if request.method == 'POST':
        file = request.FILES['csv_file']
        if not file.name.endswith('.csv'):
            return HttpResponse('This is not a CSV file')

        fs = FileSystemStorage(location='visual/data/')
        filename = fs.save(file.name, file)
        uploaded_file_url = fs.url(filename)

        # Process the CSV data
        with open('visual/data/' + filename, 'r') as csvfile:
            data = csv.reader(csvfile)
            rows = []
            for row in data:
                rows.append(row)

        # Create the Plotly chart
        with open('visual/data/' + filename, 'r') as csvfile:
            data = csv.reader(csvfile)
            x_data = []
            y_data = []
            for row in data:
                x_data.append(row[0])
                y_data.append(row[1])

        fig = go.Figure(
            data=[go.Scatter(x=x_data, y=y_data, mode='markers')]
        )

        # Render the chart and the CSV data in a template
        div = fig.to_html(full_html=False)

        return render(request, 'visual/visualization.html', {'graph': div, 'rows': rows})

    return render(request, 'visual/upload.html')





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
        if not file.name.endswith('.csv'):
            messages.error(request, 'This is not a CSV file')
            return HttpResponseRedirect(reverse('upload'))

        data, headers = process_csv(file)

        return render(request, 'visual/results.html', {'data': data, 'headers': headers})

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

