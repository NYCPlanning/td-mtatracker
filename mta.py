import pandas as pd
import plotly.express as px
import plotly.io as pio
from git import Repo
import datetime
import pytz
import time



# pio.renderers.default = "browser"
pd.set_option('display.max_columns', None)
path='/home/mayijun/GITHUB/td-plotly/'
# path='C:/Users/mayij/Desktop/DOC/GITHUB/td-plotly/'



endtime=datetime.datetime(2025,12,31,23,0,0,0,pytz.timezone('US/Eastern'))
while datetime.datetime.now(pytz.timezone('US/Eastern'))<endtime:
    timestamp=datetime.datetime.now(pytz.timezone('US/Eastern')).strftime('%m/%d/%Y')
    url="https://new.mta.info/document/20441"
    df=pd.read_csv(url,dtype=str)
    df['Date']=[datetime.datetime.strptime(x,'%m/%d/%Y') for x in df['Date']]
    df['Subway']=[int(x) for x in df['Subways: Total Estimated Ridership']]
    df['SubwayPct']=[pd.to_numeric(x.strip().replace('%',''))/100 for x in df['Subways: % Change From Prior Year Equivalent Day']]
    df['SubwayPrior']=df['Subway']/(1+df['SubwayPct'])
    df['SubwayPrior']=[int(x) for x in df['SubwayPrior']]
    df['Bus']=[int(x) for x in df['Buses: Total Estimated Ridership']]
    df['BusPct']=[pd.to_numeric(x.strip().replace('%',''))/100 for x in df['Buses: % Change From Prior Year Equivalent Day']]
    df['BusPrior']=df['Bus']/(1+df['BusPct'])
    df['BusPrior']=[int(x) for x in df['BusPrior']]
    df=df[['Date','SubwayPrior','Subway','BusPrior','Bus']].sort_values('Date').reset_index(drop=True)

    fig=px.line(df,
                x='Date',
                y=['Subway','Bus'],
                color_discrete_sequence=['tomato','steelblue'],
                title='<b>Subway and Bus Estimated Ridership '+df.iloc[0,0].strftime('%m/%d/%Y')+' - '+df.iloc[-1,0].strftime('%m/%d/%Y')+' (Source: '+"</b><a href='https://new.mta.info/coronavirus/ridership'>MTA</a>"+'<b>)</b>',
                template='plotly_white')
    fig.update_layout(
        title={'font':{'family':'arial',
                       'size':20,
                       'color':'black'},
               'x':0.5,
               'xanchor':'center'},
        legend={'orientation':'h',
                'title':{'text':''},
                'font':{'family':'arial',
                        'size':18,
                        'color':'black'},
                'x':0.5,
                'xanchor':'center'},
        xaxis={'title':{'text':'Date',
                        'font':{'family':'arial',
                                'size':16,
                                'color':'black'}},
               'tickfont':{'family':'arial',
                           'size':14,
                           'color':'black'},
               'fixedrange':True,
               'showgrid':True},
        yaxis={'title':{'text':'Ridership',
                        'font':{'family':'arial',
                                'size':16,
                                'color':'black'}},
               'tickfont':{'family':'arial',
                           'size':14,
                           'color':'black'},
               'rangemode':'nonnegative',
               'fixedrange':True,
               'showgrid':True},
        dragmode=False,
        hovermode='x unified'
    )
    fig.update_traces(
        line={'width':3},
        hovertemplate='%{y:#.3s}'
        )
    fig.write_html(path+'index.html',include_plotlyjs='cdn')
    
    repo = Repo(path)
    repo.git.add('index.html')
    repo.index.commit('autoupdate')
    origin = repo.remote(name='origin')
    origin.push()
    print(str(timestamp))
    time.sleep(86400)
