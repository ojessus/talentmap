import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(layout="wide")
a=0.623
b=0.377
df=pd.read_csv('models/HBAxoSim.csv')
dfall=df.groupby('BU').agg({'Empleados':'sum',
    'BajasT':'sum',
    '% PM':'mean',
    'COSTONOMMEN':'sum',
    'CostoPMPE':'mean',
    'CostoRPEP':'mean'}).reset_index()
dfall['Rotacion']=100*(dfall['BajasT']/(a*dfall['Empleados']+b*dfall['BajasT']))

def get_pies(data):
    costos=['% Empleados']+[ i for i in data.columns.to_list() if '% Costo' in i]
    if 'Marca' in data.columns.to_list():
        subc='Marca'
    else:
        subc='BU'
    # Create subplots: use 'domain' type for Pie subplot
    fig = make_subplots(rows=1, cols=len(costos), specs=[[{'type':'domain'} for i in range(len(costos))]])
    labels = df=data[subc].to_list()
    i=1
    for c in costos:
        fig.add_trace(go.Pie(labels=labels,insidetextorientation='radial',textinfo='percent',values=data[c].to_list(), name=c),1, i)
        i=i+1
    # Use `hole` to create a donut-like pie chart
    fig.update_traces(hole=.4, hoverinfo="label+name+percent")
    fig.update_layout(
            title_text="Porcentajes por "+subc,
            uniformtext_minsize=12, uniformtext_mode='hide',
            autosize=True
            )
    return fig

def get_hbm(data,grupo,datao):
  if grupo in ['BU1','BU2','BU3','BU4','BU5']:
    dfs=data[data.BU==grupo].copy()
  else:
    dfs=data.copy()
  B=(a*dfs.Rotacion*dfs.Empleados)/(100-b*dfs.Rotacion)
  PM = dfs['% PM']*B
  dfs['Costo Nomina']=dfs.COSTONOMMEN*12
  dfs['Costo Nominap']=dfs.COSTONOMMEN*12*(1+(datao.Rotacion-dfs.Rotacion)/150)
  dfs['Costo Nomina']=[max(i,j) for i,j in dfs[['Costo Nomina','Costo Nominap']].values]
  dfs['Costo Reclutamiento']=B*dfs.CostoRPEP
  dfs['Costo Productividad']=PM*dfs['CostoPMPE']
  dfs['Costo Total']=dfs['Costo Reclutamiento']+dfs['Costo Productividad']+dfs['Costo Nomina']
  dfs['% Empleados']=100*dfs['Empleados']/dfs['Empleados'].sum()
  dfs['% Hiring Budget Reclutamiento']=100*dfs['Costo Reclutamiento']/dfs['Costo Nomina']
  dfs['% Hiring Budget Productividad']=100*dfs['Costo Productividad']/(dfs['Costo Nomina'])
  dfs['% Hiring Budget Total']=100*(dfs['Costo Productividad']+dfs['Costo Reclutamiento'])/dfs['Costo Nomina']
  dfs['% Costo Nomina']=100*dfs['Costo Nomina']/dfs['Costo Nomina'].sum()
  dfs['% Costo Reclutamiento']=100*dfs['Costo Reclutamiento']/dfs['Costo Reclutamiento'].sum()
  dfs['% Costo Productividad']=100*dfs['Costo Productividad']/dfs['Costo Productividad'].sum()
  dfs['% Costo Totat']=100*dfs['Costo Total']/dfs['Costo Total'].sum()
  return dfs.sort_values(by='Costo Total',ascending=False)

def get_rott(datao,datap,t):
    Bo=(a*datao.Rotacion*datao.Empleados)/(100-b*datao.Rotacion)
    Bp=(a*datap.Rotacion*datap.Empleados)/(100-b*datap.Rotacion)
    roto =100*( Bo.sum()/(a*datao.Empleados.sum()+b*Bo.sum()))
    rotv = 100*( Bp.sum()/(a*datao.Empleados.sum()+b*Bp.sum()))
    fig = go.Figure(go.Indicator(
        mode = "number+delta",
        value = round(rotv,2),
        number = {'suffix': "%"},
        title = {"text": 'Rotación Voluntaria '+t},
        delta = {'reference': round(roto,2),
            'decreasing':{'color':'green'},
            'increasing':{'color':'red'}},
        domain = {'x': [0, 1], 'y': [0, 1]}))
    return fig

def get_indc(datao,datap,t):
    tam=20
    vals=dict()
    costos=['Costo Nomina',
            'Costo Reclutamiento',
            'Costo Productividad',
            'Costo Total'
            ]
    hb=['% Hiring Budget Reclutamiento',
        '% Hiring Budget Productividad',
        '% Hiring Budget Total'
        ]
    fig = go.Figure()
    Bo=(a*datao.Rotacion*datao.Empleados)/(100-b*datao.Rotacion)
    Bp=(a*datap.Rotacion*datap.Empleados)/(100-b*datap.Rotacion)
    roto =100*( Bo.sum()/(a*datao.Empleados.sum()+b*Bo.sum()))
    rotv = 100*( Bp.sum()/(a*datao.Empleados.sum()+b*Bp.sum()))
    fig.add_trace(go.Indicator(
                mode = "number+delta",
                value = round(rotv,2),
                number = {'suffix': "%"},
                title = {"text": 'Rotación Voluntaria '+t},
                delta = {'reference': round(roto,2),
                    'decreasing':{'color':'green'},
                    'increasing':{'color':'red'}
                    },
                domain = {'row': 0, 'column': 0}))
    i=0
    vals['Rotación Voluntaria']=round(rotv,2)
    vals['rvd']=round(roto,2)
    for c in costos:
        costop=datap[c].sum()
        costor=datao[c].sum()
        fig.add_trace(go.Indicator(
            mode = "number+delta",
            value = round(costop,0),
            number = {'prefix':'$', 'valueformat':",.2f"},
            delta = {'reference': round(costor,0),
                'decreasing':{'color':'green'},
                'increasing':{'color':'red'},
                'valueformat':"$,.0f"
                },
            title = {"text": "<span style='font-size:0.6em;color:gray'>{title}</span>".format(title=c)},
            domain = {'row': 1, 'column': i}))
        i=i+1
    i=1
    for c in hb:
        costop=datap[c].mean()
        costor=datao[c].mean()
        fig.add_trace(go.Indicator(
        mode = "number+delta",
        value = round(costop,2),
        number = {'valueformat':",.2f"},
        delta = {'reference': round(costor,2),
            'decreasing':{'color':'green'},
            'increasing':{'color':'red'}
            },
        title = {"text": "<span style='font-size:0.6em;color:gray'>{title}</span>".format(title=c)},
        domain = {'row': 2, 'column': i}))
        i=i+1
                                            
    fig.update_layout(
                grid = {'rows': 3, 'columns': len(costos),'pattern': "independent"}
                )
    return fig

vsv=st.selectbox('Selecciona  la BU',['Todos','BU1','BU2','BU3','BU4','BU5'])
sliders=[]
if vsv=='Todos':
    dfapt=get_hbm(dfall,vsv,dfall)
    dfaptc=dfapt.copy()
    dfsl=dfaptc[['BU','Rotacion']]
    for label,value in dfsl.values:
        sliders.append(st.slider(label=label,min_value=1.0,max_value=dfsl.Rotacion.max()+10,value=value,step=1.0))
    dfu=pd.DataFrame({'Rotacion':sliders})
    dfu.index=dfapt.index
    dfapt.update(dfu)
    dfapt=get_hbm(dfapt,vsv,dfaptc)
    #st.write(dfapt)
    #st.write(dfu)
    figp=get_pies(dfapt)
    costo=get_indc(dfaptc,dfapt,vsv)
else:
    dfapt=get_hbm(df,vsv,df)
    dfaptc=dfapt.copy()
    dfsl=dfaptc[['Marca','Rotacion']]
    for label,value in dfsl.values:
        sliders.append(st.slider(label=label,min_value=1.0,max_value=dfsl.Rotacion.max()+10,value=value,step=1.0))
    dfu=pd.DataFrame({'Rotacion':sliders})
    dfu.index=dfapt.index
    dfapt.update(dfu)
    dfapt=get_hbm(dfapt,vsv,dfaptc)
    #st.write(dfapt)
    #st.write(dfu)
    figp=get_pies(dfapt)
    costo=get_indc(dfaptc,dfapt,vsv)


st.plotly_chart(costo,use_container_width=True,height=800)
st.plotly_chart(figp,use_container_width=True)
