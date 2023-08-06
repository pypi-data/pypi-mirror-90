# Timeseries labeling
A very simple python tool using plotly and dash for labeling/marking events in timeseries.
The timeseries csv-file is assumed to have two columns, first representing the time/index and the second the corresponding value.

## Installation
Clone the repo and then from inside the repo folder run
`python setup.py install` (possibly within your virtual env)

## Running
Run command `tsl` from your terminal (have to be python env that you installed the package)
Open `http://127.0.0.1:8050/` in your browser

## Usage
Drag and drop a csv file into file selection area. Points in the timeseries can be marked either by clicking on them or by using the selection tool in plotly (box or lasso).
Once happy, click save button. Annotated files end up in a created annotated folder with the same filename as the input csv but appended with "_annotated" and a datetime. 