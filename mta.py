import pandas as pd
import numpy as np
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
from git import Repo
import datetime
import pytz
import time



# pio.renderers.default = "browser"
pd.set_option('display.max_columns', None)
path='/home/mayijun/GITHUB/td-mtatracker/'
# path='C:/Users/mayij/Desktop/DOC/GITHUB/td-mtatracker/'



endtime=datetime.datetime(2025,12,31,23,0,0,0,pytz.timezone('US/Eastern'))
while datetime.datetime.now(pytz.timezone('US/Eastern'))<endtime:
    timestamp=datetime.datetime.now(pytz.timezone('US/Eastern')).strftime('%m/%d/%Y')
    url='https://new.mta.info/document/20441'
    df=pd.read_csv(url,dtype=str)
    df['Date']=[datetime.datetime.strptime(x,'%m/%d/%Y') for x in df['Date']]
    df['Subway']=[int(x) for x in df['Subways: Total Estimated Ridership']]
    df['Bus']=[int(x) for x in df['Buses: Total Estimated Ridership']]
    df=df[['Date','Subway','Bus']].sort_values('Date').reset_index(drop=True)
    fig=px.line(data_frame=df,
                x='Date',
                y=['Subway','Bus'],
                color_discrete_sequence=['tomato','steelblue'],
                title='<b>Subway and Bus Estimated Ridership '+df.iloc[0,0].strftime('%m/%d/%Y')+' - '+df.iloc[-1,0].strftime('%m/%d/%Y')+' (Source: '+"</b><a href='https://new.mta.info/coronavirus/ridership'>MTA</a>"+'<b>)</b>',
                template='plotly_white')
    fig.update_layout(
        title={'font_size':20,
               'x':0.5,
               'xanchor':'center'},
        legend={'orientation':'h',
                'title_text':'',
                'font_size':16,
                'x':0.5,
                'xanchor':'center',
                'y':1,
                'yanchor':'bottom'},
        xaxis={'title':{'text':'Date',
                        'font_size':14},
               'tickfont_size':12,
               'fixedrange':True,
               'showgrid':True},
        yaxis={'title':{'text':'Ridership',
                        'font_size':14},
               'tickfont_size':12,
               'rangemode':'nonnegative',
               'fixedrange':True,
               'showgrid':True},
        font={'family':'Arial',
              'color':'black'},
        dragmode=False,
        hovermode='x unified'
    )
    fig.update_traces(
        line={'width':2},
        hovertemplate='%{y:#.3s}'
        )
    fig.write_html(path+'index.html',include_plotlyjs='cdn')
    
    
    
    timestamp=datetime.datetime.now(pytz.timezone('US/Eastern')).strftime('%m/%d/%Y')
    url='https://new.mta.info/document/20441'
    df=pd.read_csv(url,dtype=str)
    df['Date']=[datetime.datetime.strptime(x,'%m/%d/%Y') for x in df['Date']]
    df=df.sort_values(['Date']).reset_index(drop=True)
    df['Week']=[str(x.week)+'|'+str(x.year) for x in df['Date']]
    wkstart=df[['Week','Date']].drop_duplicates(['Week'],keep='first').reset_index(drop=True)
    wkstart['Date1']=wkstart['Date'].dt.strftime('%m/%d/%Y')
    wkend=df[['Week','Date']].drop_duplicates(['Week'],keep='last').reset_index(drop=True)
    wkend['Date2']=wkend['Date'].dt.strftime('%m/%d/%Y')
    wk=pd.merge(wkstart[['Week','Date1']],wkend[['Week','Date2']],how='inner',on='Week')
    wk['DateRange']=wk['Date1']+' - '+wk['Date2']    
    df['Subway']=pd.to_numeric(df['Subways: Total Estimated Ridership'])
    df['SubwayPct']=[pd.to_numeric(x.strip().replace('%',''))/100 for x in df['Subways: % Change From Prior Year Equivalent Day']]
    df['SubwayPrior']=df['Subway']/(1+df['SubwayPct'])
    df['Bus']=pd.to_numeric(df['Buses: Total Estimated Ridership'])
    df['BusPct']=[pd.to_numeric(x.strip().replace('%',''))/100 for x in df['Buses: % Change From Prior Year Equivalent Day']]
    df['BusPrior']=df['Bus']/(1+df['BusPct'])    
    df['LIRR']=pd.to_numeric(df['LIRR: Total Estimated Ridership'])
    df['LIRRPct']=[pd.to_numeric(x.strip().replace('%',''))/100 if pd.notna(x) else np.nan for x in df['LIRR: % Change From 2019 Monthly Weekday/Saturday/Sunday Average']]
    df['LIRRPrior']=df['LIRR']/(1+df['LIRRPct'])    
    df['MNR']=pd.to_numeric(df['Metro-North: Total Estimated Ridership'])
    df['MNRPct']=[pd.to_numeric(x.strip().replace('%',''))/100 if pd.notna(x) else np.nan for x in df['Metro-North: % Change From 2019 Monthly Weekday/Saturday/Sunday Average']]
    df['MNRPrior']=df['MNR']/(1+df['MNRPct'])    
    df['AAR']=pd.to_numeric(df['Access-A-Ride: Total Scheduled Trips'])
    df['AARPct']=[pd.to_numeric(x.strip().replace('%',''))/100 for x in df['Access-A-Ride: % Change From 2019 Monthly Weekday/Saturday/Sunday Average']]
    df['AARPrior']=df['AAR']/(1+df['AARPct'])    
    df['BT']=pd.to_numeric(df['Bridges and Tunnels: Total Traffic'])
    df['BTPct']=[pd.to_numeric(x.strip().replace('%',''))/100 for x in df['Bridges and Tunnels: % Change From Prior Year Equivalent Day']]
    df['BTPrior']=df['BT']/(1+df['BTPct'])    
    df=df.groupby(['Week'],as_index=False).agg({'Subway':'sum','SubwayPrior':'sum',
                                                'Bus':'sum','BusPrior':'sum',
                                                'LIRR':'sum','LIRRPrior':'sum',
                                                'MNR':'sum','MNRPrior':'sum',
                                                'AAR':'sum','AARPrior':'sum',
                                                'BT':'sum','BTPrior':'sum'}).reset_index(drop=True)
    df['Subway']=(df['Subway']-df['SubwayPrior'])/df['SubwayPrior']
    df['Bus']=(df['Bus']-df['BusPrior'])/df['BusPrior']
    df['Long Island Rail Road']=(df['LIRR']-df['LIRRPrior'])/df['LIRRPrior']
    df['Metro-North Railroad']=(df['MNR']-df['MNRPrior'])/df['MNRPrior']
    df['Access-A-Ride']=(df['AAR']-df['AARPrior'])/df['AARPrior']
    df['Bridges and Tunnels']=(df['BT']-df['BTPrior'])/df['BTPrior']    
    df=pd.merge(df,wk,how='inner',on='Week')
    df['Date']=[datetime.datetime.strptime(x,'%m/%d/%Y') for x in df['Date2']]
    df=df[['Date','DateRange','Subway','Bus','Long Island Rail Road','Metro-North Railroad',
           'Access-A-Ride','Bridges and Tunnels']].sort_values(['Date']).reset_index(drop=True)
    dfcolors={'Subway':'#1f77b4',
              'Bus':'#ff7f0e',
              'Long Island Rail Road':'#2ca02c',
              'Metro-North Railroad':'#d62728',
              'Access-A-Ride':'#9467bd',
              'Bridges and Tunnels':'#8c564b'}
    dfnotes={'Subway':'*',
             'Bus':'*',
             'Long Island Rail Road':'**',
             'Metro-North Railroad':'**',
             'Access-A-Ride':'**',
             'Bridges and Tunnels':'*'}
    fig=go.Figure()
    fig=fig.add_trace(go.Scattergl(name='',
                                   x=df['Date'],
                                   y=df['Subway'],
                                   opacity=0,
                                   showlegend=False,
                                   hovertext='<b>'+df['DateRange']+'</b>',
                                   hoverinfo='text'))
    for i in ['Subway','Bus','Long Island Rail Road','Metro-North Railroad','Access-A-Ride','Bridges and Tunnels']:
        fig=fig.add_trace(go.Scattergl(name=i+dfnotes[i]+'   ',
                                       mode='lines',
                                       x=df['Date'],
                                       y=df[i],
                                       line={'color':dfcolors[i],
                                             'width':2},
                                       hovertext=[i+': '+'{0:.1%}'.format(x) for x in df[i]],
                                       hoverinfo='text'))
        fig=fig.add_trace(go.Scattergl(name='',
                                       mode='markers',
                                       x=[df.loc[len(df)-1,'Date']],
                                       y=[df.loc[len(df)-1,i]],
                                       marker={'color':dfcolors[i],
                                               'size':8},
                                       showlegend=False,
                                       hoverinfo='skip'))
    fig.update_layout(
        template='plotly_white',
        title={'text':'<b>MTA Estimated Weekly Ridership Change from Previous Year (Source: '+"</b><a href='https://new.mta.info/coronavirus/ridership'>MTA</a>"+'<b>)</b>',
               'font_size':20,
               'x':0.5,
               'xanchor':'center'},
        legend={'orientation':'h',
                'title_text':'',
                'font_size':16,
                'x':0.5,
                'xanchor':'center',
                'y':1,
                'yanchor':'bottom'},
        xaxis={'title':{'text':'<b>Date</b>',
                        'font_size':14},
               'tickfont_size':12,
               'dtick':'M1',
               'fixedrange':True,
               'showgrid':False},
        yaxis={'title':{'text':'<b>Percent Change</b>',
                        'font_size':14},
               'tickfont_size':12,
               'tickformat':'.0%',
               'fixedrange':True,
               'showgrid':False},
        hoverlabel={'font_size':14},
        font={'family':'Arial',
              'color':'black'},
        dragmode=False,
        hovermode='x unified',
        )   
    fig.add_annotation(
        text='* Percent Change From Prior Year Equivalent Day     ** Percent Change From 2019 Monthly Weekday/Saturday/Sunday Average',
        font_size=12,
        xref='paper',
        x=0.5,
        xanchor='center',
        yref='paper',
        y=1,
        yanchor='top',
        showarrow=False
        )
    fig.write_html(path+'index2.html',include_plotlyjs='cdn')
    
    repo = Repo(path)
    repo.git.add('index.html')
    repo.index.commit('autoupdate')
    origin = repo.remote(name='origin')
    origin.push()
    print(str(timestamp))
    time.sleep(86400)