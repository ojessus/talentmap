import streamlit as st
import pandas as pd
import numpy as np
def rowStyle(row):
    if row['#Empleados Activos'] == '6162':
        return ['background-color: #E8F0F2'] * len(row)
    return [''] * len(row)

def highlight_max(cell):
    w=float(cell)
    
    if type(w) != str and round(w,2) < 0 :
        return 'color: green'
    elif type(w) != str and round(w,2) > 0:
        return 'color: red'
    else:
        return 'color: black'        #return 'color: black'

st.set_page_config(layout="wide")
df=pd.read_csv("models/HiringByPositionNV4.csv")
vsv=st.selectbox('VP',['Todos','VP BU1','VP BU2','VP BU3','VP BU4','VP MERCADOTECNIA'])
if vsv !='Todos':
    df=df.query("Vp=='{filtro}'".format(filtro=vsv))
ajuste={
    'PDV OFF PRICE':1.4,
    'CEDIS':1.7,
    'PDV FULL PRICE':1.4,
    'CORPORATIVO FULL PRICE':1.7,
    'CORPORATIVO OFF PRICE':1.7
}

df['SueldoP']=[i*ajuste[j] for i,j in df[['SueldoP','CLASIFICACIÓN']].values ]
df['Costo Nomina']=df['Activos']*df['SueldoP']
df['%HB']=[(i/j)*100 if j >0 else 0 for i,j in zip(df['Costo ReclutamientoP'],df['Costo Nomina'])]
df['Costo ReclutamientoP']=df['Vacantes PA']*df['Reclutamiento']
HBD = df.copy().groupby('CLASIFICACIÓN').agg({'Costo Nomina':np.sum,'Costo ReclutamientoP':np.sum,'Costo Productividad':np.sum})
HB = 100*HBD['Costo ReclutamientoP']/HBD['Costo Nomina']
HBI = 100*(HBD['Costo ReclutamientoP']+HBD['Costo Productividad'])/HBD['Costo Nomina']
oldv=df['Vacantes PA'].copy()
paramsP={ 'CORPORATIVO':374.0,
         'CORPORATIVO OFF PRICE':64.0,
         'PDV FULL PRICE':2332.0,
         'PDV OFF PRICE':4348.0,
         'CEDIS':408.0,
         'CORPORATIVO FULL PRICE':609.0	
       }
paramsA={ 'CORPORATIVO':694,
         'CORPORATIVO OFF PRICE':191,
         'PDV FULL PRICE':2359,
         'PDV OFF PRICE':2695,
         'CEDIS':190
       }
paramsV={'CORPORATIVO':374,
         'CORPORATIVO OFF PRICE':45,
         'PDV FULL PRICE':2338.0,
         'PDV OFF PRICE':3693.0,
         'CEDIS':352.0
       }

def r3(pn,nf,pf):
    return round((nf)*(pn/pf),1)

offp=st.slider('ROTACIÓN VOLUNTARIA OFF PRICE', min_value=1, max_value=200, value=120,step=1)
fp=st.slider('ROTACIÓN VOLUNTARIA FULL PRICE', min_value=1, max_value=200, value=43,step=1)
df['Vacantes PA']=[r3(offp,i,120) if 'OFF' in j else r3(fp,i,43)  for i,j in zip(oldv,df['CLASIFICACIÓN'])]
df['Costo ReclutamientoP']=df['Vacantes PA']*df['Reclutamiento']
df['Costo Productividad']=df['Vacantes PA']*df['Productividad']
dff=df.groupby('CLASIFICACIÓN').agg({'Activos':np.sum,
                                     'Costo Nomina':np.sum,
                                     'Vacantes PA':np.sum,
                                     'Costo ReclutamientoP':np.sum,
                                     'Costo Productividad':np.sum
                                     })
ic=dff.index.to_list()+['Total']
dff=dff.append(dff.sum(numeric_only=True), ignore_index=True).assign(Clasificacion=ic).set_index('Clasificacion')
dff['HB']=(dff['Costo ReclutamientoP']/dff['Costo Nomina'])*100
dff['HBI']=((dff['Costo ReclutamientoP']+dff['Costo Productividad'])/dff['Costo Nomina'])*100
dff['Diferencia HB']=dff['HB']-HB
dff['Diferencia HBI']=dff['HBI']-HBI
colsl=['Activos','SueldoP','Vacantes PA','Reclutamiento','HB','Diferencia','Costo Productividad','HBI']
titl=['#Empleados Activos','Sueldo promedio','#Vacante promedio anual','Costo de Reclutamiento','Costo Productividad','%Hiring Budget','%Hiring Budget Indirecto','Diferencia HB','Diferencia HBI']
dff.columns=titl
dff.reset_index(inplace=True)
dff=dff[(dff['Clasificacion'].str.contains('FULL')|dff['Clasificacion'].str.contains('OFF'))].rename(columns={'Clasificacion':'Clasificación'})
dff.set_index('Clasificación',inplace=True)
totales=pd.DataFrame(dff.sum()).transpose()
totales['%Hiring Budget']=(totales['Costo de Reclutamiento']/totales['Sueldo promedio'])*100
totales['%Hiring Budget Indirecto']=((totales['Costo de Reclutamiento']+totales['Costo Productividad'])/totales['Sueldo promedio'])*100
totales.index=['Total']
totales['Diferencia HB']=dff['Diferencia HB'].mean()
tchida=pd.concat([dff,totales])
tchida['Sueldo promedio']=tchida['Sueldo promedio'].map('${:,.2f}'.format)
tchida['Costo de Reclutamiento']=tchida['Costo de Reclutamiento'].map('${:,.2f}'.format)
tchida['Costo Productividad']=tchida['Costo Productividad'].map('${:,.2f}'.format)
tchida['#Empleados Activos']=tchida['#Empleados Activos'].map('{:.0f}'.format)
tchida['#Vacante promedio anual']=tchida['#Vacante promedio anual'].map('{:.2f}'.format)
tchida['%Hiring Budget']=tchida['%Hiring Budget'].map('{:.3f}'.format)
tchida['Diferencia HB']=tchida['Diferencia HB'].map('{:.3f}'.format)
tchida['Diferencia HBI']=tchida['Diferencia HBI'].map('{:.3f}'.format)
tchida['%Hiring Budget Indirecto']=tchida['%Hiring Budget Indirecto'].map('{:.3f}'.format)
st.table(tchida.style.apply(rowStyle, axis=1).applymap(highlight_max,subset=['Diferencia HB','Diferencia HBI']))
