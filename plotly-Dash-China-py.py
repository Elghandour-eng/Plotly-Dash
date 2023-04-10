#!/usr/bin/env python
# coding: utf-8

# # **China Plotly Dash**
# 
# ---

# # `01` Fetch Data

# In[2]:


THEME = 'plotly_white'


# ### `i` Import Necessary Libraries

# In[3]:


import pandas as pd # to handle dataframes
import matplotlib.pyplot as plt # to make plots

# plotly
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
# jupyter-dash
from jupyter_dash import JupyterDash
# html
from dash import html
import dash_bootstrap_components as dbc


# ### `ii` Read & Pre process the Data

# ### `Population Data`

# In[4]:


df = pd.read_csv('Data/China demographics 1965-2050.csv', na_values='..')
df


# In[5]:


df.isna().sum()


# In[6]:


# Interpolating to fill missing values 
df = df.interpolate('linear')
df.isna().sum()


# In[7]:


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
    
#     'Year': 'date',
#     'Population, total [SP.POP.TOTL]': 'Population',
#     'Population growth (annual %) [SP.POP.GROW]': 'Annual Growth Rate',
#     'Birth rate, crude (per 1,000 people) [SP.DYN.CBRT.IN]': 'Births per 1000 People',
#     'Death rate, crude (per 1,000 people) [SP.DYN.CDRT.IN]' : 'Deaths per 1000 People',
#     'Net migration [SM.POP.NETM]': 'Net Migration',
#     'Urban population (% of total population) [SP.URB.TOTL.IN.ZS]': 'Urban Population Percentage',
#     'Rural population (% of total population) [SP.RUR.TOTL.ZS]': 'Rural Population Percentage',
#     'Sex ratio at birth (male births per female births) [SP.POP.BRTH.MF]': 'Sex ratio at birth M/F',
#     'Population ages 65 and above (% of total population) [SP.POP.65UP.TO.ZS]': 'Population Above 65 Percentage',
#     'Fertility rate, total (births per woman) [SP.DYN.TFRT.IN]': 'Fertility Rate',
#     'Age dependency ratio (% of working-age population) [SP.POP.DPND]': 'Age Dependency Ratio',
#     'Mortality rate, infant (per 1,000 live births) [SP.DYN.IMRT.IN]': 'Infant Mortality Rate'
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


# In[8]:


df = df.rename(columns=columns_names)[columns_reordered]
df


# ### `Pyramid Data`

# In[9]:


#pyramid_data =pd.read_excel("Data/china-population-pyramid-1960-2050.xls ", sheet_name="Data") # sheet_name="Data" to read only data
pyramid_data = pd.read_csv("Data/china-population-pyramid-1960-2050.csv",)


# In[10]:


# Explore Pyramid data
pyramid_data.head()


# In[11]:


pyramid_data = pyramid_data[pyramid_data['Year']>=1969].reset_index(drop=True)


# In[12]:


pyramid_data.describe()


# In[13]:


pyramid_data.columns # print columns


# In[14]:


pyramid_data.columns[1:22] #first group for females 


# In[15]:


pyramid_data.columns[22:44] #first group for males 


# In[16]:


# as values is 47,920,315.00 we need to remove the comma and the dot
pyramid_data = pyramid_data.replace(',','', regex=True) #regex=True to replace all commas


# In[17]:


#convert all values to float
pyramid_data = pyramid_data.astype(float)


# In[18]:


# final we want to check that no data is missing and distribution of data
pyramid_data.info()


# ### `GDP Data`

# In[19]:


gdp = pd.read_csv('Data/China-gdpPerCapita-1960-2022.csv')
gdp


# In[20]:


gdp.info()


# In[21]:


gdp = gdp.rename(columns= {'Time' : "Year", 'GDP per capita (constant 2015 US$)':'GDP Per Capita'})


# ### `iv` Implement Plotly  

# In[22]:


df.columns


# In[23]:


fig_style = ['ggplot2', 'seaborn', 'simple_white', 'plotly',
         'plotly_white', 'plotly_dark', 'presentation', 'xgridoff',
         'ygridoff', 'gridon', 'none']


# `Figure of Popualtion` 

# In[24]:


#year > 2023 is the projection data
#year < 2023 is the historical data
merge_df = df.loc[df.Year <= 2023]
merge_df2 = df.loc[df.Year >= 2023]

merge_df_65 = df.loc[df.Year <= 2023]
merge_df2_65 = df.loc[df.Year >= 2023]

fig = go.FigureWidget(data=[
    #add historical data before 2023
    go.Scatter(x=merge_df.Year, y=merge_df['Population'], mode='lines', line={'dash': 'solid', 'color': '#5500ff'} , name="Historical Total Population",),#add annual change to hover data
    #add projection data after 2023
    go.Scatter(x=merge_df2.Year, y=merge_df2['Population'], mode='lines', line={'dash': 'dot', 'color': '#5500ff'}, name="Projection Total Population"), #add annual change to hover data
])
#add 'Population ages 65 and above (% of total population) [SP.POP.65UP.TO.ZS]' as line to the plot from df2
fig.add_scatter(x=merge_df_65.Year, y=merge_df_65['Population Above 65 Percentage'], yaxis="y2"
                , name="Historical Population ages 65 and above", mode='lines', line=dict(color='red', width=2,  ),  )

#add 'Population ages 65 and above (% of total population) [SP.POP.65UP.TO.ZS]' as line to the plot from df2
fig.add_scatter(x=merge_df2_65.Year, y=merge_df2_65['Population Above 65 Percentage'], yaxis="y2"
                , name="Projection  Population ages 65 and above", mode='lines', line=dict(color='red', width=2,dash='dot'  ))
#change the scale of y axis to log to see the change in the population and make scale of y2 to 0-50
fig.update_layout(yaxis_type="log", yaxis2=dict(overlaying='y', side='right', range=[0, 50], title='above 65'))


#add historical data before 2023
#fig.add_vline(x=2023, line_width=3, line_dash="dash", line_color="green",  annotation_text="2023", annotation_position="top right")

#add projection data after 2023
fig.add_vrect(x0=1969, x1=2023, fillcolor="red", opacity=0.05, annotation_text="", annotation_position="top left", annotation_font_size=12)

#add projection data after 2023
fig.add_vrect(x0=2023, x1=2050, fillcolor="green", opacity=0.05, annotation_text="", annotation_position="top left", annotation_font_size=12)

#make the plot interactive
fig.update_layout(hovermode="x unified", title="China's population is getting Smaller and older", xaxis_title="Year", yaxis=dict(title="Total Population", titlefont=dict(size=20,)), template=THEME
                  ,yaxis2=dict(overlaying='y', side='right', range=[0, 50], title='Population Above 65 (%)',  titlefont=dict(size=15,))
                  )
fig.update_layout(width=950,    height=300,    margin=dict(l=80, r=50, t=50, b=50),)
#  add the legend to the plot
fig.update_layout(legend=dict(orientation="h", yanchor="top", y=1.1, xanchor="right", x=1,  traceorder="normal", font=dict(family="sans-serif", size=10, color="black"), bordercolor="Black", borderwidth=0))

 


# In[25]:


gdp


# `Birth Rate, Death Rate and Life Expectancy of China` 

# In[26]:



fig2 = go.FigureWidget(data=[
    #add historical data before 2023
    go.Scatter(x=df['Year'], y=df['Births per 1000 People'], name="Birth Rate", mode='lines',),#add annual change to hover data
    #add projection data after 2023
    go.Scatter(x=gdp['Year'], y=gdp['GDP Per Capita'], name="GDP Per Capita", yaxis='y2', mode='lines',), #add annual change to hover data

                                                                                                                                                    

])
# birth  rate 
#fig2 = px.line(df, x="Year", y="Births per 1000 People", title="", template="plotly_dark",)
fig2.update_layout(hovermode="x unified", title="Birth rates plummet as China gets wealthier", xaxis_title="Year", yaxis_title="Birth (Death) rate per 1000 person", template="plotly_dark"
                  ,yaxis2=dict(overlaying='y', side='right', title='GDP Per Capita US$')
                  )
# add death rate to fig2
#fig2.add_scatter(x=df['Year'], y=df['Deaths per 1000 People'], name="Death Rate")
#fig2.add_scatter(x=gdp['Year'], y=gdp['GDP Per Capita'], name="GDP Per Capita", yaxis='y2')
fig2.add_vrect(x0=1980, x1=1992, fillcolor="green", opacity=0.05, annotation=dict(
            x=0.1,
            y=0.9,
            xref='paper',
            yref='paper',
            text='Year: 2022',
            showarrow=False)
    )

#fig2.add_vline(x=1980, line_width=3, line_dash="dash", line_color="green",  annotation_text="Birth Control Campaign", annotation_position="top left")
fig2.add_vline(x=1985, line_width=3, line_dash="dash", line_color="green",  annotation_text="One Child Policy", annotation_position="right top")
fig2.add_vline(x=1992, line_width=3, line_dash="dash", line_color="green",  annotation_text="Start of Economic Reform", annotation_position="right top")

# add life expectancy to fig2
#fig2.add_scatter(x=df3['date'], y=df3['Life Expectancy from Birth (Years)'], name="Life Expectancy")

#add title to fig2
# add  scatter to birth rate again to make it display on legend area with color blue
#fig2.add_scatter(x=df['Year'], y=df['Births per 1000 People'], name="Birth Rate", )
                   
            #make the plot interactive
fig2.update_layout(hovermode="x unified", title="Birth rates plummet as China gets wealthier", xaxis_title="Year", yaxis_title="Birth (Death) rate per 1000 person", template="plotly_white"
                  ,yaxis2=dict(overlaying='y', side='right', title='GDP Per Capita US$'), xaxis_range = [1969,2023],
                  )




# In[27]:


fig2 = go.FigureWidget(data=[
    #add historical data before 2023
    go.Scatter(x=df['Year'], y=df['Births per 1000 People'], name="Birth Rate", mode='lines',),#add annual change to hover data
    #add projection data after 2023
    go.Scatter(x=gdp['Year'], y=gdp['GDP Per Capita'], name="GDP Per Capita", yaxis='y2', mode='lines',), #add annual change to hover data

                                                                                                                                                    

])
fig2.update_layout(hovermode="x unified", title="Birth rates plummet as China gets wealthier", xaxis_title="Year", yaxis_title="Birth rate per 1000 person", template=THEME
                  ,yaxis2=dict(overlaying='y', side='right', title='GDP Per Capita US$')
                  )
fig2.add_vrect(x0=1980, x1=1992, fillcolor="green", opacity=0.05, annotation_text="Birth Control Campaign", annotation_position="top left", annotation_font_size=12)
# fig2.add_vline(x=1980, line_width=3, line_dash="dash", line_color="green",  annotation_text="Birth Control Campaign", annotation_position="top left")
# fig2.add_vline(x=1985, line_width=3, line_dash="dash", line_color="green",  annotation_text=f"One", annotation_position="top left")
# fig2.add_vline(x=1985, line_width=3, line_dash="dash", line_color="green",  annotation_text=f"Child Policy", annotation_position="top right")
# fig2.add_vline(x=1992, line_width=3, line_dash="dash", line_color="green",  annotation_text="Start of Economic Reform", annotation_position="right top")

#make the plot interactiv
fig2.update_layout(width=600,    height=300,    margin=dict(l=80, r=50, t=50, b=50), xaxis_range = [1969,2023],)

#  add the legend to the plot
fig2.update_layout(legend=dict(orientation="h", yanchor="top", y=1.2, xanchor="right", x=1.1,  traceorder="normal", font=dict(family="sans-serif", size=10, color="black"), bordercolor="Black", borderwidth=0))


# `Figure of Dependancy Ratio` 

# In[28]:


# from amgad data
fig3 = go.Figure( )
fig3.add_trace(go.Bar(x=df["Year"], y=df["Age Dependency Ratio"], name="Age dependency ratio (% of working-age population)",
                       opacity=0.8)  )
fig3.update_layout(template='plotly_dark', title="Working-Age Dependency Ratio", xaxis_title="Year",
                   )
fig3.show()


# `Figure of Density` 

# In[29]:


# # density
# fig4 = px.scatter(merged, x="date", y=" Population per Square KM", title="Density Per KM of China", template="plotly_dark",)
# fig4.show()


# `Figure of Urban vs Rural` 

# In[30]:


#Urban vs Rural
# h stack bar chart
# Urabn vs Rural using df2 
fig10 = px.bar(df, x="Year", y=['Urban Population Percentage',
                                 'Rural Population Percentage'],
               title="Urbanization goes up as workers seek better opportunities", template="plotly_white",
               labels={"value": "Percentage", "variable": "Population Type", "Year": "Year", 
                       "Urban population (% of total population) [SP.URB.TOTL.IN.ZS]": "Urban Population",
                       "Rural population (% of total population) [SP.RUR.TOTL.ZS]": "Rural Population"})
fig10.update_layout(barmode='stack' , xaxis_title="Year", yaxis_title="Population",
                    #add legend title 
                    legend_title="",)
fig10.update_layout(width=480,    height=300)
fig10.update_layout(legend=dict(orientation="h", yanchor="bottom", y=0.9, xanchor="right", x=1,
                                    traceorder="reversed", font=dict(size=12,), ),) 

fig10.update_layout(margin=dict(l=10, r=10, t=50, b=50))

#fig10.update_layout(legend=dict(orientation="h", yanchor="top", y=1.4, xanchor="right", x=0.5,  traceorder="normal", font=dict(family="sans-serif", size=10, color="black"), bordercolor="Black", borderwidth=0))
                  
fig10.show()


# `Pyramid Figure`

# In[31]:


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
fig_py = go.Figure(data=[trace_male, trace_female])


fig_py.update_layout(
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
        
#         buttons=[dict(
#             label='Play',
#             method='animate',
#             args=[None, dict(
#                 frame=dict(duration=500, redraw=True),
#                 fromcurrent=True,
#                 mode='immediate'
#             )]
        
#         )]
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
fig_py.update_xaxes(range=[-70_000_000, 70_000_000])
fig_py.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=0.9,
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
fig_py.frames = frames

fig_py.show()


# `Gender Pie Figure`

# In[32]:


# we need to make a pie chart for each year to specify the percentage of gender 

fig_pie = go.Figure()
fig_pie.add_trace(go.Pie(labels=['Female', 'Male'], values=df[['Female Percentage', 'Male Percentage']].iloc[3]
                         ),)
fig_pie.update_traces(hoverinfo='label+value', textfont_size=10,
                      marker=dict(line=dict(color='#000000', width=1 ), ))

fig_pie.update_layout(title=f'Gender Distribution in China in {df["Year"].iloc[3]}',
    template="plotly_dark", legend_title="Gender", legend=dict(x=0.80, y=0.90,),height=500, width=800)


    


# `BANS`

# In[33]:


#BAN 1 : Total pop
#Ratio from world pop

#*********************

#BAN 2 : GDP


#*********************


# # `Implemnent Dash`

# In[34]:


from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
# dcc
from dash import dcc
# jupyter dash
from jupyter_dash import JupyterDash


# In[35]:


ban_style ={"font-family": "Helvetica","text-align":"center","color":"#1C4E80","font-size":"60px"}

ban_1 = dbc.Col([
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


# In[36]:


ban_11 = html.Div([dbc.Col([
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
    ], id='ban11')


# In[37]:


# ban_2 =dbc.Col([
#             dbc.Row([    
#                 html.H6(f"Excess Males", style={"font-family": "Helvetica","text-align":"center","font-size":"25px"})
#             ]),
#             dbc.Row([
#                 html.H6("32M", style=ban_style)
#             ]),
#             dbc.Row([
#                 html.H6(f"1.2 Male per Female", style={"font-family": "Helvetica","text-align":"center","font-size":"15px","padding-top":'5px'}),
#             ]),
#             dbc.Row([
#                 html.H6(f"Gender Ratio at Birth", style={"font-family": "Helvetica","text-align":"center","font-size":"15px", "padding-top":'5px'}),
#             ])
#         ])


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
                html.H6(f"{df['Gender ratio at birth M/F'].iloc[53]} M/F", style={"font-family": "Helvetica","text-align":"center","font-size":"35px", "padding-top":'0px', "color":"#1C4E80"}),
            ])
        ])
    ], id='ban_2')


# In[38]:


title_style ={"font-family": "Helvetica","text-align":"left","color":"black","font-size":"30px", 'padding-left':'10px'}
title = dbc.CardGroup(
        [
            dbc.Card(
                dbc.CardBody([dbc.Row([
                    html.H1("China's Demographics is a Ticking Time Bomb", style=title_style),
                    html.A(html.I(className="fab fa-github", style={"color": "black", "font-size": "30px"}),
                           href="http",
                           style={"color": "white", "font-size": "30px"},
                          ),
                ])]
            )
            )],

            style = {'margin-left':'0px','margin-right':'0px','margin-bottom':'5px', 'margin-top':'0px'},
    
        #className="mt-4 shadow",
    
)
#html.H1("China's Demographics is a Ticking Time Bomb", style=title_style)


# In[39]:


# dropdown = dcc.Dropdown(
#                 id='dropdown',
#                 options=[{'label': i, 'value': i} for i in df['Year'].unique()],
#                 value='2020', 
#                 style={'width': "40%","font-family": "Halvetica",} 
#             )


# In[40]:


graph1 = dbc.Col([
    dbc.CardGroup(
        [
            dbc.Card(
                dbc.CardBody([dcc.Graph(id='fig0', figure=fig)], style = {'padding':'0px'}),
                
            ),

        ],
        className="mt-2 shadow",
    )
], width=8)


# In[41]:


graph2 = dbc.Col([
    dbc.CardGroup(
        [
            dbc.Card(
                dbc.CardBody([dcc.Graph(id='figure1', figure=fig_py)],style= {'padding-right':'0px', 'padding-top':'0px', 'padding-bottom':'0px'}),
                
            )
        ],style= {'margin-left':'0px', 'padding-right':'0px', 'padding-top':'0px', 'padding-bottom':'0px'},
        className="mt-2 shadow",
    )
], width=3)


# In[42]:


graph3 = dbc.Col([
    dbc.CardGroup(
        [
            dbc.Card(
                dbc.CardBody([dcc.Graph(id='figure2', figure=fig2)], style = {'padding':'0px', 'margin-left':'0px'}),
                
            ),

        ],style= {'margin-left':'0px', 'padding-right':'0px', 'padding-top':'0px', 'padding-bottom':'0px'},
        className="mt-2 shadow",
    )
], width=5)


# In[43]:


graph4 = dbc.Col([
    dbc.CardGroup(
        [
            dbc.Card(
                dbc.CardBody([dcc.Graph(id='figure3', figure=fig10)], style = {'padding':'0px'}),
                
            ),

        ],
        className="mt-2 shadow",
    )
], width=3)


# In[44]:


cards_2nd = dbc.Row([graph2, graph3, graph4], style={ 'width':'100%', 'margin-left':'0px'})


# In[45]:


dropdown = dbc.Col([
    dbc.CardGroup(
        [
            dbc.Card(
                dbc.CardBody(
                    [
                        #html.H6("Year", className="card-title"),
                        dbc.Row([
                            dbc.Col([
                        html.H6("Year" ,style={"font-family":"Helvetica","padding-top":"5px",
                                                                       "font-size":"20px", "margin-top":'1px', "color":"#1C4E80"
                                                                       ,"text-align":"center"
                                                                       } ), ],  width =3),
                            dbc.Col([   
                        dcc.Dropdown(
                            id="year",
                            options=[{'label':pyramid_data["Year"].iloc[i] , 'value':i ,}
                          for i in  pyramid_data.index],
                        ) ], ),]),
                    ],className="mt-0 shadow",) ,className="mt-2 shadow",
                style={ }
                
                ) ],className="mt-0 shadow",style={"height":"100%", 'padding-right':'0px'} )  ], style = {"margin":"0px", 'padding-right':'0px'} ,width= 4, )


# In[46]:


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


# In[47]:


card1 = dbc.Col([
    dbc.CardGroup(
        [
            dbc.Card(
                dbc.CardBody([ban_11]),
                style= {'height':'222px',"width":"100%"},
            ),

        ],
        className="mt-2 shadow", id='ban_1'
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
        className="mt-2 shadow", id='ban2card'
    )
], )

slider_ban =  dbc.Row([ dbc.Col([dbc.Row([dropdown]) ,dbc.Row([card1, card2],
                                                              
                                                              ), ],  ) ], style={  'margin-left':'4px'})
cards = dbc.Row([ dbc.Col([ slider_ban ] ) ,
                 
                dbc.Col([graph1 ],style={ "margin-bottom":"10px" }) ], )


# In[48]:


title_style ={"font-family": "Helvetica","text-align":"left","color":"black","font-size":"30px", 'padding-left':'10px'}
china_flag = "https://upload.wikimedia.org/wikipedia/commons/f/fa/Flag_of_the_People%27s_Republic_of_China.svg"
title = dbc.Row([    
    dbc.Col([        
    dbc.CardGroup([
                dbc.Card(
                    dbc.CardBody([dbc.Row([
                        dbc.Col([
                        html.Img(src=china_flag, style={'height':'40px', 'width':'60px'}), ], width=1),
                        dbc.Col([
                        html.H1(" China's Demographics is a Ticking Time Bomb", style=title_style), ]),
                        #add china flag
                        
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
                                                    ], style={'padding-left':'0px', 'width':'5%'}) ,
                                                        ])


# In[49]:


header = dbc.Row([dbc.Col([html.H1("China's Demographics is a Ticking Time Bomb", style=title_style)], width=11, ),
             dbc.Col([html.A(html.I(className="fab fa-github", style={"color":
                            "black", "font-size": "30px"}),
                            href="https://github.com/Elghandour-eng/Plotly-Dash",
                            style={"color": "white", "font-size": "30px", 'text-align':'right'}, )], width=1)
], style={'margin-top':'20px', 'margin-right':'1px','margin-left':'10px'})


# In[50]:


df


# In[51]:


app = JupyterDash('asffa',external_stylesheets=[dbc.themes.BOOTSTRAP, 'https://use.fontawesome.com/releases/v5.8.1/css/all.css'] )

server = app.server
 # call back to update fig_py when year is changed
app.layout = html.Div([
    title,
    #header,
    cards,
    cards_2nd,
    html.Audio(src='https://cdn.pixabay.com/download/audio/2023/03/23/audio_42813beda9.mp3?filename=mystical-guzheng-journey-143598.mp3', autoPlay=False, controls=True, loop=False),

   # bans,
    #dropdown,    
], id='main div')

@app.callback(
    [Output(component_id='figure1', component_property='figure'), 
     Output(component_id='ban11', component_property='children'),
     Output(component_id='ban_2', component_property='children'),],
    Input(component_id='year', component_property='value')
)

def update_figure(year):
    if year == None:
        raise PreventUpdate
    else:
        ban_11 = html.Div([dbc.Col([
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
    ], id='ban_1')
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
                html.H6(f"{df['Gender ratio at birth M/F'].iloc[year]} M/F", style={"font-family": "Helvetica","text-align":"center","font-size":"35px", "padding-top":'0px', "color":"#1C4E80"}),
            ])
        ])
    ], id='ban22')

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
        fig_py = go.Figure(data=[trace_male, trace_female])


        fig_py.update_layout(
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

        #         buttons=[dict(
        #             label='Play',
        #             method='animate',
        #             args=[None, dict(
        #                 frame=dict(duration=500, redraw=True),
        #                 fromcurrent=True,
        #                 mode='immediate'
        #             )]

        #         )]
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
        fig_py.update_xaxes(range=[-70_000_000, 70_000_000])
        fig_py.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=0.9,
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
        fig_py.frames = frames
    
    return fig_py, ban_11, ban_2

app.run_server()

