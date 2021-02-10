import pandas as pd
import plotly.express as px
import plotly.io as pio
from git import Repo
import datetime


# pio.renderers.default = "browser"

path='/home/mayijun/GITHUB/td-plotly/'
# path='C:/Users/mayij/Desktop/DOC/GITHUB/td-plotly/'


timestamp=datetime.datetime.now()


url1 = "https://new.mta.info/document/20441"


df0= pd.read_csv(url1, low_memory=False)

df0['Subways: % Change From Prior Year Equivalent Day'] =df0['Subways: % Change From Prior Year Equivalent Day'].astype(str)
df0['Subways: % Change From Prior Year Equivalent Day'] = df0['Subways: % Change From Prior Year Equivalent Day'].str.replace("%","")
df0['Subways: % Change From Prior Year Equivalent Day'] = df0['Subways: % Change From Prior Year Equivalent Day'].str.replace(".","").astype(int)

df0 = df0[['Date',	'Subways: Total Estimated Ridership', 'Subways: % Change From Prior Year Equivalent Day', 'Buses: Total Estimated Ridership', 'Buses: % Change From Prior Year Equivalent Day']]


df0['Equiv Prior Year_prel']= df0['Subways: Total Estimated Ridership']/(1000 + df0['Subways: % Change From Prior Year Equivalent Day'])

df0['Equiv Prior Year'] = df0['Equiv Prior Year_prel']*1000

df0['Equiv Prior Year Subway'] = df0['Equiv Prior Year'].astype(int)

df0['Subway']= df0['Subways: Total Estimated Ridership']



df0['Buses: % Change From Prior Year Equivalent Day'] =df0['Buses: % Change From Prior Year Equivalent Day'].astype(str)
df0['Buses: % Change From Prior Year Equivalent Day'] =df0['Buses: % Change From Prior Year Equivalent Day'] + '.0'
df0['Buses: % Change From Prior Year Equivalent Day'] = df0['Buses: % Change From Prior Year Equivalent Day'].str.replace("%","")
df0['Buses: % Change From Prior Year Equivalent Day'] = df0['Buses: % Change From Prior Year Equivalent Day'].str.replace(".","").astype(int)



df0['Equiv Prior Year_prel']= df0['Buses: Total Estimated Ridership']/(1000 + df0['Buses: % Change From Prior Year Equivalent Day'])


df0['Equiv Prior Year'] = df0['Equiv Prior Year_prel']*1000

df0['Equiv Prior Year Bus'] = df0['Equiv Prior Year'].astype(int)

df0['Bus']= df0['Buses: Total Estimated Ridership'].astype(int)

df0 = df0[['Date',	'Equiv Prior Year Subway', 'Subway', 'Equiv Prior Year Bus', 'Bus']]



df0['Date'] = pd.to_datetime(df0['Date'])

#df0 = df0.query('20200229 < Date <  20210101')

df0 = df0.sort_values(by=['Date'])

max_Date = df0['Date'].iloc[-1]
max_Date =  max_Date.strftime("%m/%d/%Y")

min_Date = df0['Date'].iloc[0]
min_Date =  min_Date.strftime("%m/%d/%Y")



fig = px.line(df0, x='Date', y=['Subway', 'Bus'])



for d in fig['data']:
        if d['name'] == 'Equiv Prior Year Bus':
            d['line']['color'] = 'pink'


for d in fig['data']:
        if d['name'] == 'Equiv Prior Year Subway':
            d['line']['color'] = 'lightblue'

for d in fig['data']:
    if d['name'] == 'Bus':
        d['line']['color']='orange'

for d in fig['data']:
        if d['name'] == 'Subway':
            d['line']['color'] = 'steelblue'



fig.update_layout(margin={"r":50,"t":50,"l":50,"b":50},

    title = dict(text = 'Subway and Bus Estimated Ridership ' + min_Date + ' - ' + max_Date +' (Source: MTA)' , yanchor = 'top', xanchor = 'left'),
    coloraxis_colorbar=dict(
    title="",
    lenmode="pixels", len=200,
    yanchor="top", y=1, x=1,))


fig.update_layout(legend_title_text='Total Estimated Ridership'+str(timestamp))

fig.update_yaxes(title_text= '')

fig.show()

fig.write_html(path+'test.html',include_plotlyjs='cdn')






repo = Repo(path)
repo.git.add('test.html')
repo.index.commit('autoupdate')
origin = repo.remote(name='origin')
origin.push()
