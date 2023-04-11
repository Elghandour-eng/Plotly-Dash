#!/usr/bin/env python
# coding: utf-8

# # **China Plotly Dash**
# ---

# ## `1` Import Necessary Libraries

# In[1]:


import pandas as pd # to handle dataframes
# plotly
import plotly.graph_objects as go
import plotly.express as px
# html
from dash import html, dcc, Dash
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
# jupyter-dash
#from jupyter_dash import JupyterDash


# ## `2` Read & Pre process the Data

# ### `Population Data`

# In[2]:

df = pd.read_csv('Data/China demographics 1965-2050.csv', na_values='..')

# In[3]:



# In[4]:


# Interpolating to fill missing values 
df = df.interpolate('linear')


# In[5]:


# Renaming columns and re-arranging them
columns_names = {
    'Urban population (% of total population)': 'Urban Population Percentage',
    'Sex ratio at birth (male births per female births) ': 'Gender ratio at birth M/F',
    'Rural population (% of total population)': 'Rural Population Percentage',
    'Population, total': 'Population',
    'Population, male (% of total population) ': 'Male Percentage',
    'Population, female (% of total population)': 'Female Percentage',
    'Population growth (annual %)': 'Annual Growth Rate',
    'Population ages 65 and above (% of total population)': 'Population Above 65 Percentage',
    'Net migration': 'Net Migration',
    'Mortality rate, infant (per 1,000 live births)': 'Infant Mortality Rate',
    'Fertility rate, total (births per woman)': 'Fertility Rate',
    'Death rate, crude (per 1,000 people)': 'Deaths per 1000 People',
    'Birth rate, crude (per 1,000 people)': 'Births per 1000 People',
    'Age dependency ratio (% of working-age population)':'Age Dependency Ratio',
    
}
columns_reordered = ['Year',
                     'Population',
                     'Annual Growth Rate',
                     'Births per 1000 People',	
                     'Deaths per 1000 People',
                     'Male Percentage',
                     'Female Percentage',
                     'Gender ratio at birth M/F',
                     'Population Above 65 Percentage',
                     'Net Migration',
                     'Infant Mortality Rate',
                     'Fertility Rate',
                     'Age Dependency Ratio',
                     'Urban Population Percentage',
                     'Rural Population Percentage'
                    ]


# In[6]:


df = df.rename(columns=columns_names)[columns_reordered]


# ### `Pyramid Data`

# In[7]:


pyramid_data = pd.read_csv("Data/china-population-pyramid-1960-2050.csv",)


# In[8]:


# Explore Pyramid data


# In[9]:


pyramid_data = pyramid_data[pyramid_data['Year']>=1969].reset_index(drop=True)


# In[10]:


# In[11]:




# In[12]:





# In[13]:





# In[14]:


# as values is 47,920,315.00 we need to remove the comma and the dot
pyramid_data = pyramid_data.replace(',','', regex=True) #regex=True to replace all commas


# In[15]:


#convert all values to float
pyramid_data = pyramid_data.astype(float)


# In[16]:


# final we want to check that no data is missing and distribution of data



# ### `GDP Data`

# In[17]:


gdp = pd.read_csv('Data/China-gdpPerCapita-1960-2022.csv')



# In[18]:





# In[19]:


gdp = gdp.rename(columns= {'Time' : "Year", 'GDP per capita (constant 2015 US$)':'GDP Per Capita'})


# ## `3` Creating Figures

# ### `0` Selecting Theme

# In[20]:


THEME = 'plotly_white'


# ### `1` Figure of Popualtion 

# In[21]:


#year > 2023 is the projection data
#year < 2023 is the historical data
merge_df = df.loc[df.Year <= 2023]
merge_df2 = df.loc[df.Year >= 2023]

merge_df_65 = df.loc[df.Year <= 2023]
merge_df2_65 = df.loc[df.Year >= 2023]

fig_population = go.FigureWidget(data=[
    #add historical data before 2023
    go.Scatter(x=merge_df.Year, y=merge_df['Population'], mode='lines', line={'dash': 'solid', 'color': '#5500ff'} , name="Population",),#add annual change to hover data
    #add projection data after 2023
    go.Scatter(x=merge_df2.Year, y=merge_df2['Population'], mode='lines', line={'dash': 'dot', 'color': '#5500ff'}, name="Projected Population"), #add annual change to hover data
    #add 'Population ages 65 and above before 2023
    go.Scatter(x=merge_df_65.Year, y=merge_df_65['Population Above 65 Percentage'], yaxis="y2", name="Ages 65+ (%)", mode='lines',
               line=dict(color='red', width=2,),),
    #add 'Population ages 65 and above after 2023
    go.Scatter(x=merge_df2_65.Year, y=merge_df2_65['Population Above 65 Percentage'], yaxis="y2", name="Ages 65+ Projected (%)", mode='lines',
               line=dict(color='red', width=2,dash='dot',),),

])

#add projection data after 2023
fig_population.add_vrect(x0=1969, x1=2023, fillcolor="red", opacity=0.05, annotation_text="", annotation_position="top left", annotation_font_size=12)

#add projection data after 2023
fig_population.add_vrect(x0=2023, x1=2050, fillcolor="green", opacity=0.05, annotation_text="", annotation_position="top left", annotation_font_size=12)

#make the plot interactive
fig_population.update_layout(hovermode="x unified", title={'text':'China\'s population is getting smaller and older', 'font':dict(size=20,),}, xaxis_title="Year",
                  yaxis=dict(title={'text':'Total Population', 'font':dict(size=18,), 'standoff':0}), template=THEME,
                  yaxis2=dict(overlaying='y', side='right', range=[0, 50], title={'text':'Population Above 65 (%)', 'font':dict(size=15,), 'standoff':10},)
                  )
fig_population.update_layout(width=700,    height=300,    margin=dict(l=60, r=40, t=50, b=10),)
#  add the legend to the plot
fig_population.update_layout(legend=dict(orientation="h", yanchor="top", y=1.1, xanchor="right", x=1,  traceorder="normal", font=dict(family="sans-serif", size=10, color="black"), bordercolor="Black", borderwidth=0))

 


# ### `2` Figure of Birth Rate and GDP Per capita

# In[22]:


fig_gdp = go.FigureWidget(data=[
    #add historical data before 2023
    go.Scatter(x=df['Year'], y=df['Births per 1000 People'], name="Birth Rate", mode='lines',),#add annual change to hover data
    #add projection data after 2023
    go.Scatter(x=gdp['Year'], y=gdp['GDP Per Capita'], name="GDP Per Capita", yaxis='y2', mode='lines',), #add annual change to hover data
])

fig_gdp.update_layout(hovermode="x unified", title="Birth rates plummet as China gets wealthier", xaxis_title="Year", template=THEME,
                      yaxis=dict(title={'text':'Birth Rate (per 1000 person)', 'font':dict(size=15,), 'standoff':0}),
                      yaxis2=dict(overlaying='y', side='right', title={'text':'GDP Per Capita ($US)', 'font':dict(size=15,), 'standoff':10},),
                  )
#Mark area 1980-1992
fig_gdp.add_vrect(x0=1980, x1=1992, fillcolor="black", opacity=0.3, annotation_text="Birth Control Campaign", annotation_position="top left", annotation_font_size=12)

#make the plot interactiv
fig_gdp.update_layout(width=600, height=300, margin=dict(l=50, r=40, t=50, b=50), xaxis_range=[1969,2023],)

#  add the legend to the plot
fig_gdp.update_layout(legend=dict(orientation="v", yanchor="top", y=0.95, xanchor="right", x=0.75,  traceorder="reversed", font=dict(family="sans-serif", size=10, color="black"), bordercolor="Black", borderwidth=0))


# ### `3` Figure of Dependancy Ratio

# In[23]:


# from amgad data
fig_dependecy = go.Figure( )
fig_dependecy.add_trace(go.Bar(x=df["Year"], y=df["Age Dependency Ratio"], name="Age dependency ratio (% of working-age population)",
                       opacity=0.8)  )
fig_dependecy.update_layout(template='plotly_dark', title="Working-Age Dependency Ratio", xaxis_title="Year",
                   )



# ### `4` Figure of Urbanization Rate

# In[24]:


#Urban vs Rural
# h stack bar chart
fig_urbanization = px.bar(df, x="Year", y=['Urban Population Percentage',
                                 'Rural Population Percentage'],
               title="Urbanization goes up as workers seek better opportunities", template="plotly_white",
               labels={"value": "Percentage", "variable": "Population Type", "Year": "Year", 
                       "Urban population (% of total population) [SP.URB.TOTL.IN.ZS]": "Urban Population",
                       "Rural population (% of total population) [SP.RUR.TOTL.ZS]": "Rural Population"})
fig_urbanization.update_layout(barmode='stack' , xaxis_title="Year",
                               yaxis=dict(title={'text':'Birth Rate (per 1000 person)', 'font':dict(size=15,), 'standoff':0}),
                               xaxis=dict(title={'text':'Year', 'font':dict(size=15,), 'standoff':0}),
                    #add legend title 
                    legend_title="",)
fig_urbanization.update_layout(width=480,    height=300)
fig_urbanization.update_layout(legend=dict(orientation="v", yanchor="bottom", y=0.7, xanchor="right", x=0.5,
                                    traceorder="reversed", font=dict(size=12,), ),) 

fig_urbanization.update_layout(margin=dict(l=50, r=10, t=30, b=10))
                 



# `Pyramid Figure`

# In[25]:


# Create the trace for the male data
trace_male = go.Bar(
    x=-pyramid_data.iloc[:,22:].iloc[64],
    y=pyramid_data.columns[22:].str.replace('Male',''), # to make data in the same order and same name
    orientation='h',
    name='Male',
    marker=dict(),
    #hover data
    #make hover with positive value by adding - to x
    hovertemplate='%{y} %{x} <extra></extra>',
)

# Create the trace for the female data
trace_female = go.Bar(
    x=pyramid_data.iloc[:,1:22].iloc[64],
    y=pyramid_data.columns[1:22].str.replace('Female',''), # to make data in the same order and same name
    orientation='h',
    name='Female',
    marker=dict(),
    hovertemplate='%{y} %{x} <extra></extra>',


)

# Combine the traces into a single figure
fig_pyramid = go.Figure(data=[trace_male, trace_female])

fig_pyramid.update_layout(
    title=f'China\'s Population is Rapidly Aging',
    xaxis_title='Population',
    barmode='relative',
    bargap=.1,
    width=280,
    height=300,
    margin=dict(l=20, r=1, t=50, b=20),
    template=THEME,
    xaxis_range=[-70000000,70000000],
    xaxis=go.layout.XAxis(
        tickvals=[-60000000, -40000000, -20000000, 0, 20000000, 40000000, 60000000],                      
        ticktext=["60M", "40M", "20M", "0", "20M", "40M", '60M']
    ),
    updatemenus=[dict(
        type='buttons',
        showactive=False,
        buttons=[
            dict(
                label='Play',
                method='animate',
                args=[None, dict(
                    frame=dict(duration=300, redraw=True),
                    fromcurrent=True,
                    mode='immediate'
                )]
            ),
             dict(
                label='Pause',
                method='animate',
                args=[[None], dict(
                    frame=dict(duration=0, redraw=True),
                    mode='immediate'
                )]
            ),
            
        ], x=0.25, y=1.1,

    )],
    annotations=[
        dict(
            x=0.9,
            y=1,
            xref='paper',
            yref='paper',
            text='Year: 2022',
            showarrow=False
        ),
         dict(
            x=-0.1,
            y=1.1,
            xref='paper',
            yref='paper',
            text='age',
            showarrow=False
        )
        
    ]
)
# Set x axis range and keep it constant
fig_pyramid.update_xaxes(range=[-75_000_000, 75_000_000])

#legend
fig_pyramid.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=0.9,
                                    traceorder="normal", font=dict(size=12,), ),) 

# Add frames
frames = []
for i, year in enumerate(pyramid_data.Year):
    frame = go.Frame(
        data=[
          
            go.Bar(
                x=-pyramid_data.iloc[i,22:],
                y=pyramid_data.columns[22:].str.replace('Male',''), # to make data in the same order and same name
                orientation='h',
                name='Male',
                marker=dict(),
                #hover data
                #make hover with positive value by adding - to x
                hovertemplate='%{y} %{x} <extra></extra>',
            ),
            go.Bar(
                    x=pyramid_data.iloc[i,1:22],
                    y=pyramid_data.columns[1:22].str.replace('Female',''), # to make data in the same order and same name
                    orientation='h',
                    name='Female',
                    marker=dict(),
                    hovertemplate='%{y} %{x} <extra></extra>',
            )
        ],
        name=str(year)[:4],
        layout = go.Layout(annotations = [dict(
                                            x=0.9,
                                            y=1,
                                            xref='paper',
                                            yref='paper',
                                            text=f'Year: {str(year)[:4]}',
                                            showarrow=False
                                            ),
                                             dict(
                                                x=-0.1,
                                                y=1.1,
                                                xref='paper',
                                                yref='paper',
                                                text='age',
                                                showarrow=False
                                            )]
                          )
    )
    frames.append(frame)

# Add frames to figure
fig_pyramid.frames = frames



# `Gender Pie Figure`

# In[26]:


# we need to make a pie chart for each year to specify the percentage of gender 

fig_pie = go.Figure()
fig_pie.add_trace(go.Pie(labels=['Female', 'Male'], values=df[['Female Percentage', 'Male Percentage']].iloc[3]
                         ),)
fig_pie.update_traces(hoverinfo='label+value', textfont_size=10,
                      marker=dict(line=dict(color='#000000', width=1 ), ))

fig_pie.update_layout(title=f'Gender Distribution in China in {df["Year"].iloc[3]}',
    template="plotly_dark", legend_title="Gender", legend=dict(x=0.80, y=0.90,),height=500, width=800)


    


# ## `Implemnent Dash`

#  ### `Title`

# In[27]:


title_style ={"font-family": "Helvetica","text-align":"left","color":"black","font-size":"30px", 'padding-left':'10px'}
title = dbc.Row([    
    dbc.Col([        
    dbc.CardGroup([
                dbc.Card(
                    dbc.CardBody([dbc.Row([
                        
                      dbc.Col([
                        html.Img(src="https://upload.wikimedia.org/wikipedia/commons/f/fa/Flag_of_the_People%27s_Republic_of_China.svg"
                                 , style={'height':'40px', 'width':'60px'}), ], width=1),  
                      dbc.Col([    html.H1("China's Demographics is a Ticking Time Bomb", style=title_style), ]),
                    ])
                                ]))  ],
                style = {'margin-left':'0px','margin-right':'0px','margin-up':'0px', 'margin-top':'0px',"text-align":"center", 'padding-right':'0px'},
                className="mt-0 shadow") ], width=11, style={'padding-right':'0px'}) ,

    dbc.Col([        
    dbc.CardGroup([
                dbc.Card(
                    dbc.CardBody([dbc.Row([
                        html.A(html.I(className="fab fa-github", style={"color":
                            "black", "font-size": "30px"}),
                            href="https://github.com/Elghandour-eng/Plotly-Dash",
                            style={"color": "white", "font-size": "30px"}, ),])
                                ] )  )],
                style = {'margin-left':'0px',
                        'margin-right':'0px','margin-up':'0px', 
                        'margin-top':'0px',
                        "text-align":"center", 'padding-right':'0px', 'padding-left':'0px'},
                        className="mt-0 shadow") 
                                                    ], style={'padding-left':'0px',}) ,
                                                        ])


# ### `1st row`

# #### `BANS`

# In[28]:


dropdown = dbc.Col([
    dbc.CardGroup(
        [
        dbc.Card(
            dbc.CardBody(
                [
                dbc.Row([
                    # First column
                    dbc.Col([
                    html.H6("Year",
                            style={"font-family":"Helvetica",
                                   "padding-top":"5px","font-size":"20px",
                                   "margin-top":'1px', "color":"#1C4E80",
                                    "width":"100%","text-align":"left" } # style 
                            ), # html.H6
                    ],), # dbc.Col
        # Second column            
        dbc.Col([
                    dcc.Dropdown(
                    id="year",
                    options=[{'label':pyramid_data["Year"].iloc[i] ,
                                         'value':i ,}
                    for i in  pyramid_data.index],)   ],width=10), # dcc.Dropdown
        ]) # dbc.Row

            ],className="mt-0 shadow",) ,className="mt-2 shadow",
               ) ], # dbc.CardBody
        className="mt-0 shadow",style={"width":"100%","height":"90%", 'padding-right':'0px'} )# dbc.Card
    ], style = {"margin-right":"10px", 'padding-right':'0px'} , ) # dbc.CardGroup


# In[29]:


ban_style ={"font-family": "Helvetica","text-align":"center","color":"#1C4E80","font-size":"60px"}


# In[30]:


ban_0 = dbc.Col([
    dbc.Row([
        html.H6(f"Total Population", style={"font-family": "Helvetica","text-align":"center","font-size":"40px"})
    ]),
    
    dbc.Row([
        html.H6("1.410'B'", style=ban_style)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Row([
                html.H6(f"850k",
                    style={"font-family": "Helvetica","text-align":"right","font-size":"15px","padding-top":'5px'}
                )
            ]),
            dbc.Row([
                html.H6(f"Annual  Change",
                    style={"font-family": "Helvetica","text-align":"right","font-size":"15px","padding-top":'5px'}
                ), 
            ])
        ]),
        dbc.Col([
                html.Div([
                    html.H1("|", style = {"text-align":"center","padding-bottom":'15px',"font-size":"50px"} ) 
                    ],
                         
                         ),
                
              ] , width={"size":1},  ),
                 
                dbc.Col([
                  
                  dbc.Row([
                        html.H6(f"80%", style={"font-family": "Helvetica","text-align":"center","font-size":"15px"
                                         ,"padding-top":'5px'       
                                   
                                      }),
                         ]),
                  dbc.Row([
                      
                        html.H6(f"Percentage", style={"font-family": "Helvetica","text-align":"center","font-size":"15px"
                                              ,"padding-top":'5px'
                                      
                                      }),
                  ])
             
              ] ),
                
        ]) ,
      
        
            
        ])#,width ={ "size": 4,},)


# In[31]:


ban_1 = html.Div([dbc.Col([
            dbc.Row([    
                html.H6(f"Total Population", style={"font-family": "Helvetica","text-align":"center","font-size":"25px"})
            ]),
            dbc.Row([
                html.H6(f"{round(df['Population'].iloc[53]/1000000)}", style=ban_style)
            ]),
            dbc.Row([
                html.H6(f"Annual Change", style={"font-family": "Helvetica","text-align":"center","font-size":"15px","padding-top":'5px', 'margin=bottom':
                                                '1px'}),
            ]),
            dbc.Row([
                html.H6(f"-850000", style={"font-family": "Helvetica","text-align":"center","font-size":"35px", "padding-top":'0px', "color":"#1C4E80"}),
            ])
        ])
    ], id='ban1')


# In[32]:


ban_2 = html.Div([dbc.Col([
            dbc.Row([    
                html.H6(f"Excess Males", style={"font-family": "Helvetica","text-align":"center","font-size":"25px"})
            ]),
            dbc.Row([
                html.H6(f"{round((df['Male Percentage'].iloc[53] - 50) *0.01*df['Population'].iloc[53] / 1000000)}M", style=ban_style)
            ]),
            dbc.Row([
                html.H6(f"Gender Ratio at Birth", style={"font-family": "Helvetica","text-align":"center","font-size":"15px","padding-top":'5px', 'margin=bottom':
                                                '1px'}),
            ]),
            dbc.Row([
                html.H6(f"{round(df['Gender ratio at birth M/F'].iloc[53], 2)} M/F", style={"font-family": "Helvetica","text-align":"center","font-size":"35px", "padding-top":'0px', "color":"#1C4E80"}),
            ])
        ])
    ], id='ban2')


# In[33]:


graph_population = dbc.Col([
    dbc.CardGroup(
        [
            dbc.Card(
                dbc.CardBody([dcc.Graph(id='fig_population', figure=fig_population)], style = {'padding':'0px'}),
                #style= {'width':'900px'}
                
            ),
            

        ],
        className="mt-2 shadow",style= {'width':'720px'},
    )
], width=8)


# In[34]:


card1 = dbc.Col([
    dbc.CardGroup(
        [
            dbc.Card(
                dbc.CardBody([ban_1]),
                style= {'height':'222px',"width":"100%"},
            ),

        ],
        className="mt-2 shadow", id='ban11'
    )
],)

card2 = dbc.Col([
    dbc.CardGroup(
        [
            dbc.Card(
                dbc.CardBody([ban_2]),
                style= {'height':'222px'},
            ),

        ],
        className="mt-2 shadow", id='ban22'
    )
], )

slider_ban =  dbc.Row([ dbc.Col([dbc.Row([dropdown]) ,dbc.Row([card1, card2],
                                                              
                                                              ), ],  ) ], style={  'margin-left':'4px'})
cards = dbc.Row([ dbc.Col([ slider_ban ] ) ,
                 
                dbc.Col([graph_population ],style={ "margin-bottom":"10px" }) ], )


# ### `2nd row`

# In[35]:


graph_pyramid = dbc.Col([
    dbc.CardGroup(
        [
            dbc.Card(
                dbc.CardBody([dcc.Graph(id='fig_pyramid', figure=fig_pyramid)],style= {'padding-right':'0px', 'padding-top':'0px', 'padding-bottom':'0px'}),
                
            )
        ],style= {'margin-left':'0px', 'padding-right':'0px', 'padding-top':'0px', 'padding-bottom':'0px'},
        className="mt-2 shadow",
    )
], width=3)


# In[36]:


graph_gdp = dbc.Col([
    dbc.CardGroup(
        [
            dbc.Card(
                dbc.CardBody([dcc.Graph(id='fig_gdp', figure=fig_gdp)], style = {'padding':'0px', 'margin-left':'0px'}),
                
            ),

        ],style= {'margin-left':'0px', 'padding-right':'0px', 'padding-top':'0px', 'padding-bottom':'0px'},
        className="mt-2 shadow",
    )
], width=5)


# In[37]:


graph_urbanization = dbc.Col([
    dbc.CardGroup(
        
        [
            dbc.Card(
                dbc.CardBody([dcc.Graph(id='fig_urbanization', figure=fig_urbanization)], style = {'padding':'0px'}),
                
            ),

        ],
        className="mt-2 shadow",
    )
], width=3)


# In[38]:


cards_2nd = dbc.Row([graph_pyramid, graph_gdp, graph_urbanization], style={ 'width':'100%', 'margin-left':'0px'})


# In[39]:


app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP, 'https://use.fontawesome.com/releases/v5.8.1/css/all.css'] )

server = app.server
 # call back to update fig_py when year is changed
app.layout = html.Div([
    title,
    #header,
    cards,
    cards_2nd,
    #html.Audio(src='https://cdn.pixabay.com/download/audio/2023/03/23/audio_42813beda9.mp3?filename=mystical-guzheng-journey-143598.mp3', autoPlay=True, controls=True, loop=False), 
], id='main div')

@app.callback(
    [Output(component_id='fig_pyramid', component_property='figure'), 
     Output(component_id='ban1', component_property='children'),
     Output(component_id='ban2', component_property='children'),],
    Input(component_id='year', component_property='value')
)

def update_figure(year):
    if year == None:
        raise PreventUpdate
    else:
        ban_1 = html.Div([dbc.Col([
            dbc.Row([    
                html.H6(f"Total Population", style={"font-family": "Helvetica","text-align":"center","font-size":"25px"})
            ]),
            dbc.Row([
                html.H6(f"{round(df['Population'].iloc[year]/1000000)}M", style=ban_style)
            ]),
            dbc.Row([
                html.H6(f"Annual Change", style={"font-family": "Helvetica","text-align":"center","font-size":"15px","padding-top":'5px', 'margin=bottom':
                                                '1px'}),
            ]),
            dbc.Row([
                html.H6(f"{round((df['Population'].iloc[year] - df['Population'].iloc[year-1])/1000 )}k", style={"font-family": "Helvetica","text-align":"center","font-size":"35px", "padding-top":'0px', "color":"#1C4E80"}),
            ])
        ])
    ], id='ban1')
        ban_2 = html.Div([dbc.Col([
            dbc.Row([    
                html.H6(f"Excess Males", style={"font-family": "Helvetica","text-align":"center","font-size":"25px"})
            ]),
            dbc.Row([
                html.H6(f"{round((df['Male Percentage'].iloc[year] - 50) *0.01*df['Population'].iloc[year] / 1000000)}M", style=ban_style)
            ]),
            dbc.Row([
                html.H6(f"Gender Ratio at Birth", style={"font-family": "Helvetica","text-align":"center","font-size":"15px","padding-top":'5px', 'margin=bottom':
                                                '1px'}),
            ]),
            dbc.Row([
                html.H6(f"{round(df['Gender ratio at birth M/F'].iloc[year], 2)} M/F", style={"font-family": "Helvetica","text-align":"center","font-size":"35px", "padding-top":'0px', "color":"#1C4E80"}),
            ])
        ])
    ], id='ban2')

        # Create the trace for the male data
        trace_male = go.Bar(
            x=-pyramid_data.iloc[:,22:].iloc[year],
            y=pyramid_data.columns[22:].str.replace('Male',''), # to make data in the same order and same name
            orientation='h',
            name='Male',
            marker=dict(),
            #hover data
            #make hover with positive value by adding - to x
            hovertemplate='%{y} %{x} <extra></extra>',
        )

        # Create the trace for the female data
        trace_female = go.Bar(
            x=pyramid_data.iloc[:,1:22].iloc[year],
            y=pyramid_data.columns[1:22].str.replace('Female',''), # to make data in the same order and same name
            orientation='h',
            name='Female',
            marker=dict(),
            hovertemplate='%{y} %{x} <extra></extra>',


        )

        # Combine the traces into a single figure
        fig_pyramid = go.Figure(data=[trace_male, trace_female])


        fig_pyramid.update_layout(
            title=f'China\'s Population is Rapidly Aging',
            xaxis_title='Population',
            #yaxis_title='Age Group',
            barmode='relative',
            bargap=.1,
            width=280,
            height=300,
            margin=dict(l=20, r=1, t=50, b=50),
            template=THEME,
            xaxis_range=[-70000000,70000000],
            xaxis=go.layout.XAxis(
                tickvals=[-60000000, -40000000, -20000000, 0, 20000000, 40000000, 60000000],                      
                ticktext=["60M", "40M", "20M", "0", "20M", "40M", '60M']
            ),


            updatemenus=[dict(
                type='buttons',
                showactive=False,
                buttons=[
                    dict(
                        label='Play',
                        method='animate',
                        args=[None, dict(
                            frame=dict(duration=300, redraw=True),
                            fromcurrent=True,
                            mode='immediate'
                        )]
                    ),
                     dict(
                        label='Pause',
                        method='animate',
                        args=[[None], dict(
                            frame=dict(duration=0, redraw=True),
                            mode='immediate'
                        )]
                    ),

                ], x=0.25, y=1.1,

            )],
            annotations=[
                dict(
                    x=0.9,
                    y=1,
                    xref='paper',
                    yref='paper',
                    text=f'Year: {pyramid_data.iloc[:,0].iloc[year]}',
                    showarrow=False
                ),
                 dict(
                    x=-0.1,
                    y=1.1,
                    xref='paper',
                    yref='paper',
                    text='age',
                    showarrow=False
                )

            ]
        )
        # Set x axis range and keep it constant
        fig_pyramid.update_xaxes(range=[-70_000_000, 70_000_000])
        fig_pyramid.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=0.9,
                                            traceorder="normal", font=dict(size=12,), ),) 

        # Add frames
        frames = []
        for i, year in enumerate(pyramid_data.Year):
            frame = go.Frame(
                data=[

                    go.Bar(
                        x=-pyramid_data.iloc[i,22:],
                        y=pyramid_data.columns[22:].str.replace('Male',''), # to make data in the same order and same name
                        orientation='h',
                        name='Male',
                        marker=dict(),
                        #hover data
                        #make hover with positive value by adding - to x
                        hovertemplate='%{y} %{x} <extra></extra>',
                    ),
                    go.Bar(
                            x=pyramid_data.iloc[i,1:22],
                            y=pyramid_data.columns[1:22].str.replace('Female',''), # to make data in the same order and same name
                            orientation='h',
                            name='Female',
                            marker=dict(),
                            hovertemplate='%{y} %{x} <extra></extra>',
                    )
                ],
                name=str(year)[:4],
                layout = go.Layout(annotations = [dict(
                                                    x=0.9,
                                                    y=1,
                                                    xref='paper',
                                                    yref='paper',
                                                    text=f'Year: {str(year)[:4]}',
                                                    showarrow=False
                                                    ),
                                                     dict(
                                                        x=-0.1,
                                                        y=1.1,
                                                        xref='paper',
                                                        yref='paper',
                                                        text='age',
                                                        showarrow=False
                                                    )]
                                  )


            )
            frames.append(frame)

        # Add frames to figure
        fig_pyramid.frames = frames
    
    return fig_pyramid, ban_1, ban_2

if __name__ == '__main__':
    app.run_server(debug=False)


# %%

# %%

# %%
