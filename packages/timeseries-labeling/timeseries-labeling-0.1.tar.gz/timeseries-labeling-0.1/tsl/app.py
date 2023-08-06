import json
import base64
import io
import os

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import plotly.graph_objects as go 
import numpy as np
from datetime import datetime


from tsl.tsl_pylib.io.load_csv import csv_to_numpy
from tsl.tsl_pylib.visualization.plot import create_timeseries_with_annotations_plot

# dash html styles
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}    

# annotations 
annotations = []

def main():    

    # create a plotly figure (placeholder for the annotation)
    fig = create_timeseries_with_annotations_plot([],[],[],[])

    # create the dash app
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    app.layout = html.Div([
        html.H1('Time-series annotation',style={'text-align':'center'}),
        html.Label('',id='filename',style={'text-align':'center'}),
        dcc.Graph(
            id='ts_annotation',
            figure=fig
        ),
        html.Center(html.Button('Save annotation', id='save_file', n_clicks=0)),
        html.Hr(),
        html.H3('Select csv file for annotation',style={'text-align':'center'}),
        dcc.Upload(
        id='upload_csv',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select File')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=False #True
    )
            ])

    @app.callback(
        Output('ts_annotation','figure'),
        Output('filename','children'),
        Input('upload_csv', 'contents'),
        Input('upload_csv', 'filename'),
        Input('ts_annotation', 'selectedData'),
        Input('ts_annotation', 'clickData'),
        Input('save_file','n_clicks'),
        State('ts_annotation', 'figure'),
        State('filename','children'))
    def process_callback(contents, filename, selected_data, click_data, save_file, fig, label):
        global annotations

        # check which callback was triggered 
        ctx = dash.callback_context
        if ctx.triggered:
            context = ctx.triggered[0]['prop_id'].split('.')[0]
            if context == 'upload_csv':
                # decode csv and update figure
                _, content_string = contents.split(',')
                decoded = base64.b64decode(content_string)
                annotations = [] 
                data = csv_to_numpy(io.StringIO(decoded.decode('utf-8')))
                x = data[:,0]
                y = data[:,1]
                fig = create_timeseries_with_annotations_plot(x,y,[],[])
                label = filename
                return fig, label
            elif context == 'save_file':
                # save annotations
                if len(annotations) > 0:
                    os.makedirs('annotations',exist_ok=True)
                    date_time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
                    annotation_filename = label[:-4]+'_annotation_' + date_time + '.csv'
                    np.savetxt(os.path.join('annotations',annotation_filename),np.array(annotations),delimiter=",")
                return fig, label

        # handle annotation
        if selected_data:
            for point in selected_data['points']:
                point_xy = [point['x'],point['y']]
                if point_xy not in annotations:
                    annotations.append(point_xy)

        if click_data is not None:
            result = click_data['points']
            point = result[0]
            point_xy = [point['x'],point['y']]
            if selected_data is None:
                if point_xy in annotations:
                    # remove annotated point if present
                    del annotations[annotations.index(point_xy)]
                else:
                    # add annotated point if not present
                    annotations.append(point_xy)
            else:
                # remove annotated point if not in selection
                selected_points = [[point['x'],point['y']] for point in selected_data['points']] 
                if point_xy not in selected_points:
                    if point_xy in annotations:
                        del annotations[annotations.index(point_xy)]

        # update figure
        if len(annotations) > 0:
            fig['data'][1]['x'] = np.array(annotations)[:,0]
            fig['data'][1]['y'] = np.array(annotations)[:,1]

        return fig, label

    app.run_server(debug=False)


if __name__ == '__main__':
    main()