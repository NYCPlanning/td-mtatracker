import datetime
import pytz
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

timestamp=datetime.datetime.now(pytz.timezone('US/Eastern')).strftime('%m/%d/%Y')

try:
    url='https://data.ny.gov/resource/vxuj-8kew.csv?$limit=5000'
    df=pd.read_csv(url,dtype=str)
    df['Date']=[x.split('T')[0] for x in df['date']]
    df['Date']=[datetime.datetime.strptime(x,'%Y-%m-%d') for x in df['Date']]
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
        xaxis={'title':{'text':'<b>Date</b>',
                        'font_size':14},
               'tickfont_size':12,
               'fixedrange':True,
               'showgrid':True},
        yaxis={'title':{'text':'<b>Ridership</b>',
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
    fig.write_html('./index.html',include_plotlyjs='cdn')
    
    
    # All Transit Percentage
    url='https://data.ny.gov/api/views/vxuj-8kew/rows.csv?accessType=DOWNLOAD&sorting=true'
    df=pd.read_csv(url,dtype=str)
    df=df.replace('TBD','')
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
    # df['SubwayPct']=[pd.to_numeric(x.strip().replace('%',''))/100 for x in df['Subways: % of Comparable Pre-Pandemic Day']]
    df['SubwayPct']=pd.to_numeric(df['Subways: % of Comparable Pre-Pandemic Day'])
    df['SubwayPrior']=df['Subway']/df['SubwayPct']
    df['Bus']=pd.to_numeric(df['Buses: Total Estimated Ridership'])
    # df['BusPct']=[pd.to_numeric(x.strip().replace('%',''))/100 for x in df['Buses: % of Comparable Pre-Pandemic Day']]
    df['BusPct']=pd.to_numeric(df['Buses: % of Comparable Pre-Pandemic Day'])
    df['BusPrior']=df['Bus']/df['BusPct']
    df['LIRR']=pd.to_numeric(df['LIRR: Total Estimated Ridership'])
    # df['LIRRPct']=[pd.to_numeric(x.strip().replace('%',''))/100 if pd.notna(x) else np.nan for x in df['LIRR: % of 2019 Monthly Weekday/Saturday/Sunday Average']]
    df['LIRRPct']=pd.to_numeric(df['LIRR: % of 2019 Monthly Weekday/Saturday/Sunday Average'])
    df['LIRRPrior']=df['LIRR']/df['LIRRPct']
    df['MNR']=pd.to_numeric(df['Metro-North: Total Estimated Ridership'],errors='coerce')
    # df['MNRPct']=[pd.to_numeric(x.strip().replace('%',''),errors='coerce')/100 if pd.notna(x) else np.nan for x in df['Metro-North: % of 2019 Monthly Weekday/Saturday/Sunday Average']]
    df['MNRPct']=pd.to_numeric(df['Metro-North: % of 2019 Monthly Weekday/Saturday/Sunday Average'])
    df['MNRPrior']=df['MNR']/df['MNRPct']
    df['AAR']=pd.to_numeric(df['Access-A-Ride: Total Scheduled Trips'])
    # df['AARPct']=[pd.to_numeric(x.strip().replace('%',''))/100 for x in df['Access-A-Ride: % of Comprable Pre-Pandemic Day']]
    df['AARPct']=pd.to_numeric(df['Access-A-Ride: % of Comprable Pre-Pandemic Day'])
    df['AARPrior']=df['AAR']/df['AARPct']
    df['BT']=pd.to_numeric(df['Bridges and Tunnels: Total Traffic'])
    # df['BTPct']=[pd.to_numeric(x.strip().replace('%',''))/100 for x in df['Bridges and Tunnels: % of Comparable Pre-Pandemic Day']]
    df['BTPct']=pd.to_numeric(df['Bridges and Tunnels: % of Comparable Pre-Pandemic Day'])
    df['BTPrior']=df['BT']/df['BTPct']
    df=df.groupby(['Week'],as_index=False).agg({'Subway':'sum','SubwayPrior':'sum',
                                                'Bus':'sum','BusPrior':'sum',
                                                'LIRR':'sum','LIRRPrior':'sum',
                                                'MNR':'sum','MNRPrior':'sum',
                                                'AAR':'sum','AARPrior':'sum',
                                                'BT':'sum','BTPrior':'sum'}).reset_index(drop=True)
    df['Subway']=df['Subway']/df['SubwayPrior']
    df['Bus']=df['Bus']/df['BusPrior']
    df['Long Island Rail Road']=df['LIRR']/df['LIRRPrior']
    df['Metro-North Railroad']=df['MNR']/df['MNRPrior']
    df['Access-A-Ride']=df['AAR']/df['AARPrior']
    df['Bridges and Tunnels']=df['BT']/df['BTPrior']    
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
        title={'text':'<b>MTA Estimated Weekly Ridership as Percentage of 2019 (Source: '+"</b><a href='https://new.mta.info/coronavirus/ridership'>MTA</a>"+'<b>)</b>',
               'font_size':20,
               'x':0.5,
               'xanchor':'center',
               'y':0.98,
               'yanchor':'top'},
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
        text='* Percentage of Pre-Pandemic Equivalent Day     ** Percentage of 2019 Monthly Averages for Weekdays, Saturdays and Sundays',
        font_size=12,
        xref='paper',
        x=0.5,
        xanchor='center',
        yref='paper',
        y=1,
        yanchor='top',
        showarrow=False
        )
    fig.write_html('./index2.html',
                   include_plotlyjs='cdn',
                   config={'displaylogo':False,'modeBarButtonsToRemove':['select2d','lasso2d']})
    
    
    
    # 7-Day Moving Average
    url='https://data.ny.gov/api/views/vxuj-8kew/rows.csv?accessType=DOWNLOAD&sorting=true'
    df=pd.read_csv(url,dtype=str)
    df=df.replace('TBD','')
    df['Date']=[datetime.datetime.strptime(x,'%m/%d/%Y') for x in df['Date']]
    df=df.sort_values(['Date']).reset_index(drop=True)
    df['end']=df['Date'].dt.strftime('%m/%d/%Y')
    df['start']=np.roll(df['end'],6)
    df['DateRange']=df['start']+' - '+df['end']   
    df['Subway']=pd.to_numeric(df['Subways: Total Estimated Ridership'])
    df['SubwayPct']=pd.to_numeric(df['Subways: % of Comparable Pre-Pandemic Day'])
    df['SubwayPrior']=df['Subway']/df['SubwayPct']
    df['SubwayAvg']=df['Subway'].rolling(7,min_periods=1).mean()
    df['SubwayPriorAvg']=df['SubwayPrior'].rolling(7,min_periods=1).mean()
    df['Bus']=pd.to_numeric(df['Buses: Total Estimated Ridership'])
    df['BusPct']=pd.to_numeric(df['Buses: % of Comparable Pre-Pandemic Day'])
    df['BusPrior']=df['Bus']/df['BusPct']
    df['BusAvg']=df['Bus'].rolling(7,min_periods=1).mean()
    df['BusPriorAvg']=df['BusPrior'].rolling(7,min_periods=1).mean()
    df['LIRR']=pd.to_numeric(df['LIRR: Total Estimated Ridership'])
    df['LIRRPct']=pd.to_numeric(df['LIRR: % of 2019 Monthly Weekday/Saturday/Sunday Average'])
    df['LIRRPrior']=df['LIRR']/df['LIRRPct']
    df['LIRRAvg']=df['LIRR'].rolling(7,min_periods=1).mean()
    df['LIRRPriorAvg']=df['LIRRPrior'].rolling(7,min_periods=1).mean()
    df['MNR']=pd.to_numeric(df['Metro-North: Total Estimated Ridership'],errors='coerce')
    df['MNRPct']=pd.to_numeric(df['Metro-North: % of 2019 Monthly Weekday/Saturday/Sunday Average'])
    df['MNRPrior']=df['MNR']/df['MNRPct']
    df['MNRAvg']=df['MNR'].rolling(7,min_periods=1).mean()
    df['MNRPriorAvg']=df['MNRPrior'].rolling(7,min_periods=1).mean()
    df['AAR']=pd.to_numeric(df['Access-A-Ride: Total Scheduled Trips'])
    df['AARPct']=pd.to_numeric(df['Access-A-Ride: % of Comprable Pre-Pandemic Day'])
    df['AARPrior']=df['AAR']/df['AARPct']
    df['AARAvg']=df['AAR'].rolling(7,min_periods=1).mean()
    df['AARPriorAvg']=df['AARPrior'].rolling(7,min_periods=1).mean()
    df['BT']=pd.to_numeric(df['Bridges and Tunnels: Total Traffic'])
    df['BTPct']=pd.to_numeric(df['Bridges and Tunnels: % of Comparable Pre-Pandemic Day'])
    df['BTPrior']=df['BT']/df['BTPct']
    df['BTAvg']=df['BT'].rolling(7,min_periods=1).mean()
    df['BTPriorAvg']=df['BTPrior'].rolling(7,min_periods=1).mean()
    df['Subway']=df['SubwayAvg']/df['SubwayPriorAvg']
    df['Bus']=df['BusAvg']/df['BusPriorAvg']
    df['Long Island Rail Road']=df['LIRRAvg']/df['LIRRPriorAvg']
    df['Metro-North Railroad']=df['MNRAvg']/df['MNRPriorAvg']
    df['Access-A-Ride']=df['AARAvg']/df['AARPriorAvg']
    df['Bridges and Tunnels']=df['BTAvg']/df['BTPriorAvg']    
    df=df.loc[6:,['Date','DateRange','Subway','Bus','Long Island Rail Road','Metro-North Railroad',
                  'Access-A-Ride','Bridges and Tunnels']].sort_values(['Date']).reset_index(drop=True)
    
    dfcolors={'Subway':'rgba(114,158,206,0.8)',
              'Bus':'rgba(103,191,92,0.8)',
              'Long Island Rail Road':'rgba(237,102,93,0.8)',
              'Metro-North Railroad':'rgba(168,120,110,0.8)',
              'Access-A-Ride':'rgba(237,151,202,0.8)',
              'Bridges and Tunnels':'rgba(173,139,201,0.8)'}
    dfnotes={'Subway':'*',
         'Bus':'*',
         'Long Island Rail Road':'**',
         'Metro-North Railroad':'**',
         'Access-A-Ride':'**',
         'Bridges and Tunnels':'*'}
    fig=go.Figure()
    fig=fig.add_trace(go.Scattergl(name='',
                                   mode='none',
                                   x=df['Date'],
                                   y=df['Subway'],
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
        title={'text':'<b>MTA Estimated Ridership and Traffic as Percentage of 2019</b><br>(7-Day Moving Average)',
               'font_size':20,
               'x':0.5,
               'xanchor':'center',
               'y':0.95,
               'yanchor':'top'},
        legend={'orientation':'h',
                'title_text':'',
                'font_size':16,
                'x':0.5,
                'xanchor':'center',
                'y':1,
                'yanchor':'bottom'},
        margin = {'b': 160,
                  'l': 80,
                  'r': 40,
                  't': 140},
        xaxis={'title':{'text':'<b>Date</b>',
                        'font_size':14},
               'tickfont_size':12,
               'dtick':'M1',
               'range':[min(df['Date'])-datetime.timedelta(days=15),max(df['Date'])+datetime.timedelta(days=15)],
               'fixedrange':True,
               'showgrid':False},
        yaxis={'title':{'text':'<b>Percent Change</b>',
                        'font_size':14},
               'tickfont_size':12,
               'tickformat':'.0%',
               'fixedrange':True,
               'showgrid':False},
        hoverlabel={'bgcolor':'rgba(255,255,255,0.95)',
                    'bordercolor':'rgba(0,0,0,0.1)',
                    'font_size':14},
        font={'family':'Arial',
              'color':'black'},
        dragmode=False,
        hovermode='x unified',
        )
    fig.add_annotation(text='<i>*% of Comparable Pre-Pandemic Day</i>',
                       font_size=14,
                       showarrow=False,
                       x=1,
                       xanchor='right',
                       xref='paper',
                       y=0,
                       yanchor='top',
                       yref='paper',
                       yshift=-80)
    fig.add_annotation(text='<i>**% of 2019 Monthly Weekday/Saturday/Sunday Average</i>',
                       font_size=14,
                       showarrow=False,
                       x=1,
                       xanchor='right',
                       xref='paper',
                       y=0,
                       yanchor='top',
                       yref='paper',
                       yshift=-100)
    fig.add_annotation(text = 'Data Source: <a href="https://new.mta.info/coronavirus/ridership" target="blank">Metropolitan Transportation Authority</a>',
                       font_size=14,
                       showarrow=False,
                       x=1,
                       xanchor='right',
                       xref='paper',
                       y=0,
                       yanchor='top',
                       yref='paper',
                       yshift=-120)
    fig.write_html('./7DayAvg.html',
                   include_plotlyjs='cdn',
                   config={'displayModeBar':True,
                           'displaylogo':False,
                           'modeBarButtonsToRemove':['select',
                                                     'lasso2d']})
    
    print(timestamp+' SUCCESS!')

except:
    print(timestamp+' ERROR!')    










