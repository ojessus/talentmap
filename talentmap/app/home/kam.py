import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.graph_objects as go


def make_clickable(text, url):
    return f'<a href="{url}{text}">{text}</a>'

def get_df(name):
    df1=dfcomp.query("Nombre=='{nombre}'".format(nombre=name))[numcols+['Clase']]
    df2=pulses.query("Clase=='{clase}'".format(clase=df1.Clase.values[0]))
    df1['Pulso']=name
    df2['Pulso']='Ideal '+df1.Clase.values[0]
    return pd.concat([df1,df2])

def get_dft(name):
    df1=kamtend.query("COLABORADOR=='{nombre}'".format(nombre=name))
    return df1

numcols=[
          'Mejores prácticas',
          'Desviación positiva',
          'Desviación negativa',
          'SFIA competencias duras',
          'Desempeño',
          'Soft skills'
         ]

nocols=[
   'COLABORADOR',
   'medalla_soq',
   'medalla_kam',
   'base',
   'fx',
   'd',
   'ie_n',
   'ie_p'
]
pd.set_option('display.max_colwidth', -1)
st.set_page_config(layout="wide")
dfcomp = pd.read_csv("models/KAMSIM.csv")
dfcomp['Desviación negativa']=100-dfcomp['Desviación negativa']
pulses = pd.read_csv("models/KAMCats.csv")
pulses['Desviación negativa']=100-pulses['Desviación negativa']
kamodel = pd.read_csv("models/kammodelv1.csv")
kamprobs = pd.read_csv("models/kamprobsv1.csv")
kamtend = pd.read_csv("models/kamtend.csv")
idsl = dfcomp.Nombre.sort_values().to_list()
numemp = st.selectbox('Selecionar Colaborador', idsl, key=1)
df=get_df(numemp)
tend=get_dft(numemp)
mk=kamodel.query("COLABORADOR=='{nombre}'".format(nombre=numemp))
medalla=mk.medalla_kam.values[0] if str(mk.medalla_kam.values[0])!='0' else df.iloc[1,:]['Clase']
medallap=medalla.lower().capitalize()
proms = dfcomp.query("Clase=='{med}'".format(med=medallap))[numcols].mean() 
c1, c2,c3 = st.columns(3)
c1.text('Similitud: '+df.iloc[1,:]['Clase'])
c2.text('Jefe Puso: '+ (mk.medalla_kam.values[0] if str(mk.medalla_kam.values[0])!='0' else 'SC' ) if len(mk)>0 else 'S/C' )
c3.text('Tendencia: '+ (mk.medalla_soq.values[0] if str(mk.medalla_soq.values[0])!='0' else 'SC' ) if len(mk)>0 else 'S/C')
figi=go.Figure()
figi.add_trace(go.Indicator(
    mode = "number+delta",
    value = df.iloc[0,:]['Desviación positiva'],
    delta = {'reference': df.iloc[1,:]['Desviación positiva']},
    title = {"text": "Índice de Influencia<br><span style='font-size:0.8em;color:gray'>Positivo</span><br>"},
    domain = {'x': [0, 1], 'y': [0.7, 1]}))
figi.add_trace( go.Indicator(
    mode = "number+delta",
    value = df.iloc[0,:]['Desviación negativa'],
    delta = {'reference': df.iloc[1,:]['Desviación negativa']},
    title = {"text": "Índice de Influencia<br><span style='font-size:0.8em;color:gray'>Negativo</span><br>"},
    domain = {'x': [0, 1], 'y': [0, 0.3]}))

fig = go.Figure()
fig.add_trace(go.Scatter(y=df.iloc[0,:][numcols], x=numcols,
                    mode='lines+markers',
                    name=df.iloc[0,:]['Pulso']))
fig.add_trace(go.Scatter(y=df.iloc[1,:][numcols], x=numcols,
                    mode='lines+markers',
                    name=df.iloc[1,:]['Pulso']))
fig.add_trace(go.Scatter(y=proms.to_list(), x=numcols,
                    mode='lines+markers',
                    name='Promedio KAM ({med})'.format(med=medalla)))

#fig.update_layout(title='Clase: '+df.iloc[1,:]['Clase'], autosize=False,
#                  width=1200, height=600,
#                  margin=dict(l=40, r=40, b=40, t=40))
fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
))
fig.update_yaxes(range = [-0,100])
#st.plotly_chart(fig)

coli1, coli2 = st.columns(2)
coli1.plotly_chart(fig,use_column_width=True)
coli2.markdown("<h1 style='text-align: center;'>Influencia:</h1>", unsafe_allow_html=True)
coli2.plotly_chart(figi,use_column_width=True)

#fig2 = go.Figure()
name=numemp

# fig2.add_trace(go.Indicator(
#         mode = "number+delta", value = dfcomp.query("Nombre=='{nombre}'".format(nombre=name))['P_Oro'].values[0],
#         domain = {'y': [0.25, 1], 'x': [0.08, 0.25]},
#         title = {'text': "Oro"},
#         delta = {'reference': 100},
#         gauge = {
#             'shape': "bullet",
#             'axis': {'range': [None, 100]},
#             'bar': {'color': "black"}}))
# 
# fig2.add_trace(go.Indicator(
#         mode = "number+delta", value = dfcomp.query("Nombre=='{nombre}'".format(nombre=name))['P_Plata'].values[0],
#         domain = {'y': [0.25, 1], 'x': [0.4, 0.6]},
#         title = {'text': "Plata"},
#         delta = {'reference': 100},
#         gauge = {
#             'shape': "bullet",
#             'axis': {'range': [None, 100]},
#             'bar': {'color': "black"}}))
# 
# fig2.add_trace(go.Indicator(
#         mode = "number+delta", value = dfcomp.query("Nombre=='{nombre}'".format(nombre=name))['P_Bronce'].values[0],
#         domain = {'y': [0.25, 1], 'x': [0.7, 0.9]},
#         title = {'text' :"Bronce"},
#         delta = {'reference': 100},
#         gauge = {
#             'shape': "bullet",
#             'axis': {'range': [None, 100]},
#             'bar': {'color': "black"}}))
# fig2.update_layout(title='Potencia de Clasificación (EM)', autosize=False,
#                   width=1200, height=400,
#                   margin=dict(l=40, r=40, b=40, t=40))
# 
# st.plotly_chart(fig2)
try:
    figkp=go.Figure()
    figkp.add_trace(go.Indicator(
            mode = "number+delta", value = 100*kamprobs.query("COLABORADOR=='{nombre}'".format(nombre=name))['ORO'].values[0],
            domain = {'y': [0.25, 1], 'x': [0.08, 0.25]},
            title = {'text': "Oro"},
            delta = {'reference': 100},
            gauge = {
                'shape': "bullet",
                'axis': {'range': [None, 100]},
                'bar': {'color': "black"}}))
    
    figkp.add_trace(go.Indicator(
            mode = "number+delta", value = 100*kamprobs.query("COLABORADOR=='{nombre}'".format(nombre=name))['PLATA'].values[0],
            domain = {'y': [0.25, 1], 'x': [0.4, 0.6]},
            title = {'text': "Plata"},
            delta = {'reference': 100},
            gauge = {
                'shape': "bullet",
                'axis': {'range': [None, 100]},
                'bar': {'color': "black"}}))
    
    figkp.add_trace(go.Indicator(
            mode = "number+delta", value = 100*kamprobs.query("COLABORADOR=='{nombre}'".format(nombre=name))['BRONCE'].values[0],
            domain = {'y': [0.25, 1], 'x': [0.7, 0.9]},
            title = {'text' :"Bronce"},
            delta = {'reference': 100},
            gauge = {
                'shape': "bullet",
                'axis': {'range': [None, 100]},
                'bar': {'color': "black"}}))
    figkp.update_layout(autosize=False,
                      width=700, height=400,
                      margin=dict(l=40, r=40, b=40, t=40))

    figt = go.Figure()
    figt.add_trace(go.Scatter(
        x=[0, 0, 0],
        y=[0.1, 1.6,2.6 ],
        text=["ORO", "PLATA", "BRONCE"],
        mode="text",
        textfont=dict(
            color="black",
            size=18,
            family="Arail",
        )
    ))
    

    # Update axes properties
    figt.update_xaxes(
        showticklabels=False,
        showgrid=False,
        zeroline=False,
    )
    
    figt.update_yaxes(
        showticklabels=False,
        showgrid=False,
        zeroline=False,
    )
    
    # Add circles
    figt.add_shape(type="circle",
        line_color="orange", fillcolor="orange",
        x0=-3, y0=-3, x1=3, y1=3,
        opacity=0.2,
    
    )
    figt.add_shape(type="circle",
        line_color="silver", fillcolor="silver",
        x0=-2, y0=-2, x1=2, y1=2,
        opacity=0.2,
    
    )
    figt.add_shape(type="circle",
        line_color="gold", fillcolor="gold",
        x0=-1, y0=-1, x1=1, y1=1,
        opacity=0.2,
    
    )
    figt.add_shape(type="circle",
    x0=-2.5, y0=-2.5, x1=2.5, y1=2.5,
    line_color="orange",
    )
    figt.add_shape(type="circle",
    x0=-1.5, y0=-1.5, x1=1.5, y1=1.5,
    line_color="silver",
    )
    figt.add_shape(type="circle",
    x0=-0.5, y0=-0.5, x1=0.5, y1=0.5,
    line_color="gold",
    )
    #fig.update_shapes(opacity=0.3, xref="x", yref="y")
    figt.add_trace(go.Scatter(
        x=[tend.iloc[0,:]['x']],
        y=[tend.iloc[0,:]['y']],
        mode='markers',
        marker_symbol='star-dot',
        marker=dict(
            color='red',
            size=14,
            line=dict(
                color='red',
                width=2
            )
        )
    ))
    figt.update_layout(
        margin=dict(l=20, r=20, b=100),
        height=400, width=400,
        plot_bgcolor="white",
        showlegend=False
    )
    
    colit1, colit2 = st.columns(2)
    colit1.markdown("<h1> Mezcla: </h1>", unsafe_allow_html=True)
    colit1.plotly_chart(figkp)
    colit2.markdown("<h1> Tendencia: </h1>", unsafe_allow_html=True)
    colit2.plotly_chart(figt)
    
except:
    pass

try:
    dff = pd.DataFrame({'Variable':mk.drop(columns=nocols).columns.to_list() ,
                        'Influencia':mk.drop(columns=nocols).values[0]
                        }).query('Influencia>0').sort_values(by='Influencia').tail(10)
    dfo = pd.DataFrame({'Variable':mk.drop(columns=nocols).columns.to_list() ,
                        'Influencia':mk.drop(columns=nocols).values[0]
                        }).sort_values(by='Influencia', ascending=False).tail(10)
    fig3 = go.Figure(go.Bar(
            x=dff.Influencia.to_list(),
            y=dff.Variable.to_list(),
            text=dff.Variable.to_list(),
            textposition='inside',
            orientation='h'))
    fig3.update_layout(yaxis_visible=False, yaxis_showticklabels=False)
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig4 = go.Figure(go.Bar(
            x=dfo.Influencia.to_list(),
            y=dfo.Variable.to_list(),
            text=dfo.Variable.to_list(),
            textposition='inside',
            marker=dict(
                color='rgba(246, 78, 139, 0.6)',
                line=dict(color='rgba(246, 78, 139, 1.0)', width=3)
            ),
            orientation='h'))
    fig4.update_layout(yaxis_visible=False, yaxis_showticklabels=False)
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    st.title("En lo que tiene que trabajar es:")
    col1, col2 = st.columns(2)
    col1.header("Hay una alta percepción de:")
    col1.plotly_chart(fig3,use_column_width=True)
    col2.header("Hay una baja percepción de:")
    col2.plotly_chart(fig4,use_column_width=True)
except:
    st.title(name + ' no se encuentra en el modelo KAM')
    

