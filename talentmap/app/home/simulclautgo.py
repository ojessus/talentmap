import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

st.set_page_config(layout="wide")
df=pd.read_csv('models/ClautgoSim.csv')
st.write('1. Información de la organización – Datos demográficos')
colsl1 = st.beta_columns(3)
expind=colsl1[0].beta_expander('1.1. Industria:')
industry={i:expind.checkbox(label=i,value=True) for i in df.M02_INDUSTRIANM.drop_duplicates().to_list()}
exptp=colsl1[1].beta_expander('1.2. Tipo de propiedad:')
tprop={i:exptp.checkbox(label=i,value=True) for i in df[df.M02_INDUSTRIANM.isin([i for i,j in industry.items() if j])].M02_TIPOPROPIEDADNM.dropna().drop_duplicates().to_list()}
exptorg=colsl1[2].beta_expander('1.3. Tipo de organización:')
tporg={i:exptorg.checkbox(label=i,value=True) for i in df[
        (df.M02_INDUSTRIANM.isin([i for i,j in industry.items() if j])) & (df.M02_TIPOPROPIEDADNM.isin([i for i,j in tprop.items() if j]))
        ].M02_TIPOORGANIZACIONNM.dropna().drop_duplicates().to_list()}
colsl2=st.beta_columns(3)
exptop=colsl2[0].beta_expander('1.4. Tiempo de operación:')
tiop={i:exptop.checkbox(label=i,value=True) for i in df[
                (df.M02_INDUSTRIANM.isin([i for i,j in industry.items() if j])) & 
                (df.M02_TIPOPROPIEDADNM.isin([i for i,j in tprop.items() if j])) &
                (df.M02_TIPOORGANIZACIONNM.isin([i for i,j in tporg.items() if j]))
                ].M02_TIEMPOOPERACIONNM.dropna().drop_duplicates().to_list()}
exppi=colsl2[1].beta_expander('1.5. Parque industrial:')
parque={i:exppi.checkbox(label=i,value=True) for i in df[
                (df.M02_INDUSTRIANM.isin([i for i,j in industry.items() if j])) & 
                (df.M02_TIPOPROPIEDADNM.isin([i for i,j in tprop.items() if j])) &
                (df.M02_TIPOORGANIZACIONNM.isin([i for i,j in tporg.items() if j]))&
                (df.M02_TIEMPOOPERACIONNM.isin([i for i,j in tiop.items() if j]))
                ].M02_PARQUEINDUSTRIALNM.dropna().drop_duplicates().to_list()}
exploc=colsl2[2].beta_expander('1.6. Localidad:')
local={i:exploc.checkbox(label=i,value=True,key=i) for i in df[ 
                (df.M02_INDUSTRIANM.isin([i for i,j in industry.items() if j])) & 
                (df.M02_TIPOPROPIEDADNM.isin([i for i,j in tprop.items() if j])) &
                (df.M02_TIPOORGANIZACIONNM.isin([i for i,j in tporg.items() if j]))&
                (df.M02_TIEMPOOPERACIONNM.isin([i for i,j in tiop.items() if j])) &
                (df.M02_PARQUEINDUSTRIALNM.isin([i for i,j in parque.items() if j]))
                ].M02_LOCALIDADNM.dropna().drop_duplicates().to_list()}
colsl3=st.beta_columns(3)
expoc=colsl3[0].beta_expander('1.7. Origen del capital:')
capital={i:expoc.checkbox(label=i,value=True,key=i+'cap') for i in df[
                (df.M02_INDUSTRIANM.isin([i for i,j in industry.items() if j])) &
                (df.M02_TIPOPROPIEDADNM.isin([i for i,j in tprop.items() if j])) &
                (df.M02_TIPOORGANIZACIONNM.isin([i for i,j in tporg.items() if j]))&
                (df.M02_TIEMPOOPERACIONNM.isin([i for i,j in tiop.items() if j])) &
                (df.M02_PARQUEINDUSTRIALNM.isin([i for i,j in parque.items() if j]))&
                (df.M02_LOCALIDADNM.isin([i for i,j in local.items() if j]))  
                ].M02_ORIGENCAPITALNM.dropna().drop_duplicates().to_list()}
expre=colsl3[1].beta_expander('1.8. Rango de operación:')
rangoe={i:expre.checkbox(label=i,value=True,key=i+'re') for i in df[
                (df.M02_INDUSTRIANM.isin([i for i,j in industry.items() if j])) &
                (df.M02_TIPOPROPIEDADNM.isin([i for i,j in tprop.items() if j])) &
                (df.M02_TIPOORGANIZACIONNM.isin([i for i,j in tporg.items() if j]))&
                (df.M02_TIEMPOOPERACIONNM.isin([i for i,j in tiop.items() if j])) &
                (df.M02_PARQUEINDUSTRIALNM.isin([i for i,j in parque.items() if j]))&
                (df.M02_LOCALIDADNM.isin([i for i,j in local.items() if j]))&
                (df.M02_ORIGENCAPITALNM.isin([i for i,j in capital.items() if j]))
                ].M02_TIEMPOOPERACIONNM.dropna().drop_duplicates().to_list()}
exptier=colsl3[2].beta_expander('1.9. Tier')
tier={i:exptier.checkbox(label=i,value=True,key=i+'re') for i in df[
                (df.M02_INDUSTRIANM.isin([i for i,j in industry.items() if j])) &
                (df.M02_TIPOPROPIEDADNM.isin([i for i,j in tprop.items() if j])) &
                (df.M02_TIPOORGANIZACIONNM.isin([i for i,j in tporg.items() if j]))&
                (df.M02_TIEMPOOPERACIONNM.isin([i for i,j in tiop.items() if j])) &
                (df.M02_PARQUEINDUSTRIALNM.isin([i for i,j in parque.items() if j]))&
                (df.M02_LOCALIDADNM.isin([i for i,j in local.items() if j]))&
                (df.M02_ORIGENCAPITALNM.isin([i for i,j in capital.items() if j]))&
                (df.M02_TIEMPOOPERACIONNM.isin([i for i,j in rangoe.items() if j]))
                ].M02_TIERNM.dropna().drop_duplicates().to_list()}

data=df[
        (df.M02_INDUSTRIANM.isin([i for i,j in industry.items() if j])) &
        (df.M02_TIPOPROPIEDADNM.isin([i for i,j in tprop.items() if j])) &
        (df.M02_TIPOORGANIZACIONNM.isin([i for i,j in tporg.items() if j]))&
        (df.M02_TIEMPOOPERACIONNM.isin([i for i,j in tiop.items() if j])) &
        (df.M02_PARQUEINDUSTRIALNM.isin([i for i,j in parque.items() if j]))&
        (df.M02_LOCALIDADNM.isin([i for i,j in local.items() if j]))&
        (df.M02_ORIGENCAPITALNM.isin([i for i,j in capital.items() if j]))&
        (df.M02_TIEMPOOPERACIONNM.isin([i for i,j in rangoe.items() if j]))
        ]
if any(tier.values()):
    data=data[data.M02_TIERNM.isin([i for i,j in tier.items() if j])]
st.write('2. Información de los empleados')
with st.beta_expander('2.1. Empleados representados:'):
    colsip=['AÑO',
            'SEMESTRE']
    colsip2=[
            'M03_ADMINISTRATIVO_PLANTA_SINDIC',
            'M03_ADMINISTRATIVO_PLANTA_SINDICNO',
            'M03_ADMINISTRATIVO_EVENTUAL_SINDIC',
            'M03_ADMINISTRATIVO_EVENTUAL_SINDICNO',
            'M03_OPERADOR_PLANTA_SINDIC',
            'M03_OPERADOR_PLANTA_SINDICNO',
            'M03_OPERADOR_EVENTUAL_SINDIC',
            'M03_OPERADOR_EVENTUAL_SINDICNO'
            ]
    df1=data[colsip+colsip2].copy()
    data1=pd.DataFrame()
    for c in colsip2:
        cs = c.split('_')
        puesto=cs[1]
        contrato=cs[2]
        representado=cs[3]
        con=df1[colsip].copy()
        con['Puesto']=puesto
        con['Contrato']=contrato
        con['Representación']=representado
        con['#Empleados']=df1[c].values
        con['Representación']=con['Representación'].fillna('SIN INFORMACIÓN')
        data1=pd.concat([data1,con])
    data1=data1.fillna(0)
    data1['Representación']=data1['Representación'].map({'SINDIC':'SINDICALIZADO','SINDICNO':'NO SINDICALIZADO'})
    data1['SEMESTRE']=data1['SEMESTRE'].map({'Primer':'Primer Semestre','Segundo':'Segundo Semestre'})
    fig = px.treemap(data1, path=[px.Constant("Año"),'AÑO', 'SEMESTRE','Representación','Puesto','Contrato'], 
                             values='#Empleados',color='Representación')
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))

    figtabs = make_subplots(rows=2, 
            subplot_titles=('ADMINISTRATIVOS','OPERADORES'),
            shared_xaxes=True,
            vertical_spacing=0.1,
            specs=[[{"type": "table"}],
                   [{"type": "table"}]
                  ]
            )
    tabad=data1[data1.Puesto=='ADMINISTRATIVO'].groupby(['AÑO','SEMESTRE','Representación','Contrato']).agg({'#Empleados':'sum'}).reset_index().pivot(index=['AÑO','SEMESTRE','Contrato'],columns='Representación',values='#Empleados').reset_index()
    tabop=data1[data1.Puesto=='OPERADOR'].groupby(['AÑO','SEMESTRE','Representación','Contrato']).agg({'#Empleados':'sum'}).reset_index().pivot(index=['AÑO','SEMESTRE','Contrato'],columns='Representación',values='#Empleados').reset_index()
    figtabs.add_trace(
        go.Table(header=dict(values=tabad.columns.to_list()),
                                     cells=dict(values=tabad.values.T)),
        row=1,
        col=1
        )
    figtabs.add_trace(
        go.Table(header=dict(values=tabop.columns.to_list()),
                                    cells=dict(values=tabop.values.T)),
        row=2,
        col=1
     )
    figtabs.update_layout(height=600)
    st.plotly_chart(fig,use_container_width=True)
    st.plotly_chart(figtabs,use_container_width=True)

with st.beta_expander('2.2. Distribución de género por nivel '):
    colsip=['AÑO',
            'SEMESTRE'
            ]
    colsip2=[
            'M03_DIRECTOR_GENERO_H',
            'M03_DIRECTOR_GENERO_M',
            'M03_GERENTE_GENERO_H',
            'M03_GERENTE_GENERO_M',
            'M03_ADMINISTRATIVO_GENERO_H',
            'M03_ADMINISTRATIVO_GENERO_M',
            'M03_TECNICO_GENERO_H',
            'M03_TECNICO_GENERO_M',
            'M03_OPERADOR_GENERO_H',
            'M03_OPERADOR_GENERO_M'
            ]
    df2=data[colsip+colsip2]
    dfge=pd.DataFrame()
    for c in colsip2:
        cs=c.split('_')
        puesto=cs[1]
        genero=cs[-1]
        dft=df2[colsip]
        dft['Puesto']=puesto
        dft['Genero']=genero
        dft['%Empleados']=df2[c].values
        dfge=pd.concat([dfge,dft])
    dfge.Genero=dfge.Genero.map({'H':'Hombre','M':'Mujer'})
    dfge['SEMESTRE']=dfge['SEMESTRE'].map({'Primer':'Primer Semestre','Segundo':'Segundo Semestre'})
    dfge['Encuesta']=[str(i)+'-'+str(j) for i,j in dfge[colsip].values]
    figen = px.sunburst(dfge, path=['Encuesta', 'Puesto', 'Genero'], values='%Empleados')
    figen.update_traces(textinfo="label")
    st.plotly_chart(figen,use_container_width=True)

with st.beta_expander('2.3. Acciones sobre plantilla'):
    colac=['AÑO', 'SEMESTRE', 'M03_VARIACION_PCT', 'M03_PLANTILLAACCIONNM']
    df3=data[colac].copy()
    df3.M03_VARIACION_PCT=df3.M03_VARIACION_PCT.fillna(0)
    df3.M03_PLANTILLAACCIONNM= df3.M03_PLANTILLAACCIONNM.fillna('Sin cambios')
    df3=df3.groupby(['AÑO', 'SEMESTRE', 'M03_PLANTILLAACCIONNM']).agg({'M03_VARIACION_PCT':'mean'}).reset_index()
    st.table(df3)
#with st.beta_expander('6. Prestaciones garantizadas'):
#    st.write("hello")
#with st.beta_expander('7. Prestaciones no garantizadas'):
#    st.write("hello")
st.write('8. Indicadores semestrales – Información predictiva')
with st.beta_expander('8.1 Rotación'):
    components.iframe('https://app.powerbi.com/view?r=eyJrIjoiZmVhZmM2ZjktNjY1MS00MWZlLWE5NjAtODU4MmM1ZmRiYjdlIiwidCI6ImZmNjRmZWUwLWZmZWYtNGQxOS1iNzM2LTJjNDA4YzA3ODgzMyJ9', height=600)
#with st.beta_expander('9. Mejores prácticas de RH'):
#    st.write("hello")
#with st.beta_expander('10. Operación diaria de RH'):
#    st.write("hello")
#with st.beta_expander('11. Esquemas de trabajo - Nuevo'):
#    st.write("hello")
