import pandas as pd 
import numpy as np   
import dash  
import dash_core_components as dcc 
import dash_html_components as html  
import plotly.graph_objs as go 
import json 

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('./data/longform.csv', index_col = 0)

app.layout = html.Div([
    html.Div([
        html.H3('都道府県別人口とGDP,一人当たりGDP', style={
            'textAlign': 'center'
        }),
        html.Div(id='hover-data-test'),
        html.Div([
            dcc.Graph(id = 'scatter-chart',
                      hoverData = {'points': [{'customdata': '大阪府'}]},
            ),
            dcc.Slider(
                id = 'slider-one',
                min = df['year'].min(),
                max = df['year'].max(),
                marks = {i: '{}'.format(i) for i in range(int(df['year'].min()), int(df['year'].max())) if i % 2 == 1},
            )
        ])
    ])
])

@app.callback(
    dash.dependencies.Output('scatter-chart', 'figure'),
    [dash.dependencies.Input('slider-one', 'value')]
)
def update_graph(selected_year):
    dff = df[df['year'] == selected_year]
    dffper = dff[dff['item']=='pergdp']
    dffgdp = dff[dff['item']== 'GDP']
    dffpop = dff[dff['item']== 'popu']

    return {
        'data': [go.Scatter(
            x = dffper[dffper['area']==i]['value'],
            y = dffgdp[dffgdp['area']==i]['value'],
            mode = 'markers',
            customdata = [i],
            marker={
                'size' : dffpop[dffpop['area']==i]['value']/100,
                'color': dffpop[dffpop['area']==i]['value']/10000,
            }, 
            name=i,
        )for i in dff.area.unique()],
        'layout': {
            'height': 600,
            #'width': 2000,
            'xaxis': {
                'type': 'log',
                'title': '都道府県別一人当たりGDP(log scale)',
                'range':[np.log(80), np.log(1200)]
            },
            'yaxis': {
                'type':'log',
                'title': '都道府県別GDP(log scale)',
                'range':[np.log(80), np.log(8000)]
            },
            'hovermode': 'closest',
        }
    }

@app.callback(
    dash.dependencies.Output('hover-data-test', 'children'),
    [(dash.dependencies.Input('scatter-chart', 'hoverData'))]
)
def datatest(hoverdata):
    return json.dumps(hoverdata)


if __name__=="__main__":
    app.run_server(debug=True)