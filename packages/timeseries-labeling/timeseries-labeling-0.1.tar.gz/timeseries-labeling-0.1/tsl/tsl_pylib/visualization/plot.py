import numpy as np
import plotly.graph_objects as go 
    
def create_timeseries_with_annotations_plot(x: np.ndarray, y: np.ndarray, x_a: np.ndarray, y_a: np.ndarray, marker_size: int=10):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y,
                    mode='lines+markers',
                    name='signal',
                    marker = dict(color='rgba(0, 0, 255, .1)', size=marker_size,
                        line=dict(color='MediumPurple',width=2)),
                    selected_marker = dict(color='rgba(0, 0, 255, .1)', size=marker_size),
                    unselected_marker = dict(color='rgba(0, 0, 255, .1)', size=marker_size)))
    fig.add_trace(go.Scatter(x=x_a, y=y_a,
                    mode='markers',
                    name='annotation', marker_color='rgba(255, 0, 0, .9)', marker_size=marker_size,
                    selected_marker = dict(color='rgba(255, 0, 0, .9)', size=marker_size),
                    unselected_marker = dict(color='rgba(255, 0, 0, .9)', size=marker_size)))
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(clickmode='event+select')

    return fig
