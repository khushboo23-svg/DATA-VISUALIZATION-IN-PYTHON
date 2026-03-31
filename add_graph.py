# =========================
# IMPORT REQUIRED LIBRARIES
# =========================

# Pandas → used for reading and processing dataset
import pandas as pd

# Plotly Graph Objects → used for creating detailed/custom graphs
import plotly.graph_objects as go

# Dash framework
import dash

# Dash core components (interactive elements like input, graph)
from dash import dcc

# Dash HTML components (UI elements like div, h1)
from dash import html

# Used for creating callbacks (input → output connection)
from dash.dependencies import Input, Output


# =========================
# LOAD DATASET
# =========================

# Read airline dataset from URL
# encoding → ensures proper reading of special characters
# dtype → forces some columns to be read as string (important for consistency)
airline_data = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv',
    encoding="ISO-8859-1",
    dtype={
        'Div1Airport': str, 
        'Div1TailNum': str,
        'Div2Airport': str, 
        'Div2TailNum': str
    }
)


# =========================
# CREATE DASH APPLICATION
# =========================

# Initialize Dash app
app = dash.Dash(__name__)


# =========================
# DEFINE APP LAYOUT (UI)
# =========================

# Layout defines what will be visible on the webpage
app.layout = html.Div(children=[ 

    # -------------------------
    # TITLE OF DASHBOARD
    # -------------------------
    html.H1(
        'Airline Performance Dashboard',
        style={
            'textAlign': 'center',   # center align text
            'color': '#503D36',      # text color
            'font-size': 40          # font size
        }
    ),

    # -------------------------
    # INPUT FIELD (YEAR INPUT)
    # -------------------------
    html.Div([

        # Label text
        "Input Year: ",

        # Input box for user to enter year
        dcc.Input(
            id='input-year',        # unique id (used in callback)
            value='2010',           # default value
            type='number',          # numeric input only
            style={
                'height': '50px', 
                'font-size': 35     # size of input box text
            }
        ),

    ],
    style={'font-size': 40}  # style for whole input section
    ),

    # Line breaks for spacing
    html.Br(),
    html.Br(),

    # -------------------------
    # GRAPH COMPONENT
    # -------------------------
    # This is where the line graph will be displayed
    html.Div(
        dcc.Graph(id='line-plot')  # graph id used in callback
    ),

])


# =========================
# CALLBACK (CORE LOGIC)
# =========================

# Callback connects input → output
# When user changes input year → function runs automatically

@app.callback(

    # OUTPUT: update graph figure
    Output(component_id='line-plot', component_property='figure'),

    # INPUT: value from input box
    Input(component_id='input-year', component_property='value')
)


# =========================
# FUNCTION FOR GRAPH UPDATE
# =========================

def get_graph(entered_year):

    # -------------------------
    # FILTER DATA
    # -------------------------
    # Select rows where Year == entered_year
    # Convert entered_year to int (important)
    df = airline_data[airline_data['Year'] == int(entered_year)]
    

    # -------------------------
    # GROUP DATA
    # -------------------------
    # Group data by Month
    # Calculate average arrival delay (ArrDelay)
    line_data = df.groupby('Month')['ArrDelay'].mean().reset_index()


    # -------------------------
    # CREATE LINE GRAPH
    # -------------------------
    fig = go.Figure(

        # Scatter plot (used for line graph)
        data=go.Scatter(
            x=line_data['Month'],        # X-axis → Month
            y=line_data['ArrDelay'],     # Y-axis → Avg Delay
            mode='lines',                # line graph
            marker=dict(color='green')   # line color
        )
    )


    # -------------------------
    # UPDATE GRAPH LAYOUT
    # -------------------------
    fig.update_layout(
        title='Month vs Average Flight Delay Time',
        xaxis_title='Month',
        yaxis_title='ArrDelay'
    )


    # -------------------------
    # RETURN GRAPH
    # -------------------------
    # This graph is sent to Output → displayed on screen
    return fig


# =========================
# RUN THE APPLICATION
# =========================

if __name__ == '__main__':

    # Starts Dash server
    # Opens app at http://127.0.0.1:8050/
    app.run(debug=True)