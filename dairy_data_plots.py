import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Read the dataset
df = pd.read_csv("C:\\Users\\etsij\\Desktop\\Data_Visulization\\main_project\\dairy_dataset.csv")

# Initialize the app
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Custom CSS styles
external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Define the layout for each page
app.layout = html.Div(style={'backgroundColor': '#F0E68C'}, children=[
    html.Div([
        html.Div([
            dcc.Location(id='url', refresh=False),
            dcc.Link('Shelf Life vs. Quantity in Stock', href='/page2', className='btn btn-primary mb-2'),
            dcc.Link('Customer Location Distribution', href='/page3', className='btn btn-primary mb-2'),
            dcc.Link('Product Revenue by Brand', href='/page4', className='btn btn-primary mb-2'),
            dcc.Link('Stock Management', href='/page5', className='btn btn-primary mb-2')
        ], className='col-md-3 text-center align-self-center'),
        html.Div(id='page-content', className='col-md-9 text-center align-self-center')
    ], className='row justify-content-center align-items-center')
])

# Description of the Dairy Data Analysis
description = html.Div([
    html.H1('Explore the Dairy Goods Sales Dataset', className='mt-5', style={'color': 'brown'}),
    html.P("The Dairy Goods Sales Dataset offers a rich and detailed exploration into the world of dairy farming, product sales, and inventory management. Spanning from 2019 to 2022, this dataset provides a comprehensive look into various aspects such as farm location, land area, cow population, production dates, product details, sales information, and more. With a focus on selected dairy brands across specific regions in India, the analysis aims to unravel key insights into sales and distribution patterns, the impact of storage conditions and shelf life on product quality, and the performance of dairy farms based on location and population. Through this multi-page Dash app, delve into the intriguing world of dairy data analysis and uncover valuable insights driving the dairy industry forward.", className='lead', style={'color': 'brown'})
])

# Define layout for page 2: Shelf Life vs. Quantity in Stock
page2_layout = html.Div([
    html.H1('Shelf Life vs. Quantity in Stock', className='mt-5', style={'color': 'brown'}),
    dcc.Graph(id='shelf-life-vs-stock-graph'),
], className='container')

# Define layout for page 3: Customer Location Distribution
page3_layout = html.Div([
    html.H1('Customer Location Distribution', className='mt-5', style={'color': 'brown'}),
    dcc.Graph(id='customer-location-graph'),
], className='container')

# Define layout for page 4: Product Revenue by Brand
page4_layout = html.Div([
    html.H1('Product Revenue by Brand', className='mt-5', style={'color': 'brown'}),
    dcc.Graph(id='product-revenue-graph'),
], className='container')

# Define layout for page 5: Stock Management
page5_layout = html.Div([
    html.H1('Stock Management', className='mt-5', style={'color': 'brown'}),
    dcc.Graph(id='stock-management-graph'),
], className='container')

# Callback to update page content based on URL
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page2':
        return page2_layout
    elif pathname == '/page3':
        return page3_layout
    elif pathname == '/page4':
        return page4_layout
    elif pathname == '/page5':
        return page5_layout
    else:
        return description

# Callback to update Shelf Life vs. Quantity in Stock graph
@app.callback(
    Output('shelf-life-vs-stock-graph', 'figure'),
    [Input('url', 'pathname')]
)
def update_shelf_life_vs_stock_graph(pathname):
    if pathname == '/page2':
        fig = px.scatter(df, x='Shelf Life (days)', y='Quantity in Stock (liters/kg)', title='Shelf Life vs. Quantity in Stock')
        return fig

# Callback to update Customer Location Distribution graph
@app.callback(
    Output('customer-location-graph', 'figure'),
    [Input('url', 'pathname')]
)
def update_customer_location_graph(pathname):
    if pathname == '/page3':
        customer_location_distribution = df['Customer Location'].value_counts()
        fig = px.pie(values=customer_location_distribution.values, names=customer_location_distribution.index, title='Customer Location Distribution')
        return fig

# Callback to update Product Revenue by Brand graph
@app.callback(
    Output('product-revenue-graph', 'figure'),
    [Input('url', 'pathname')]
)
def update_product_revenue_graph(pathname):
    if pathname == '/page4':
        revenue_by_brand = df.groupby('Brand')['Approx. Total Revenue(INR)'].sum().reset_index()
        fig = px.bar(revenue_by_brand, x='Brand', y='Approx. Total Revenue(INR)', title='Product Revenue by Brand')
        return fig

# Callback to update Stock Management graph
@app.callback(
    Output('stock-management-graph', 'figure'),
    [Input('url', 'pathname')]
)
def update_stock_management_graph(pathname):
    if pathname == '/page5':
        fig = px.bar(df, x='Product Name', y=['Quantity in Stock (liters/kg)', 'Minimum Stock Threshold (liters/kg)', 'Reorder Quantity (liters/kg)'],
                     barmode='group', title='Stock Management')
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
