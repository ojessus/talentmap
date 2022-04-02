import streamlit as st
import pandas as pd
import numpy as np
st.set_page_config(layout="wide")
df=pd.read_csv("models/HiringByPositionN.csv")
#HB=df['%HB'].copy()
#HBT = 100*df['Costo ReclutamientoP'].sum()/df['Costo Nomina'].sum()
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
@st.cache(allow_output_mutation=True)
def rowStyle(row):
    if row.Empresa == 'Total':
        return ['background-color: #E8F0F2'] * len(row)
    return [''] * len(row)

def highlight_max(cell):
    cell=float(cell)
    if type(cell) != str and cell < 0 :
        return 'color: green'
    elif cell > 0:
        return 'color: red'
    else:
        return 'color: black'

def get_dataframe():
    return pd.DataFrame(
        np.random.randn(50, 20),
        columns=('col %d' % i for i in range(20)))



# Create row, column, and value inputs

# Change the entry at (row, col) to the given value

# And display the result!
puesto=st.selectbox('Selecionar Puesto',df.Puesto.drop_duplicates().to_list(), key=1)
colsl=['Empresa','CLASIFICACIÓN','Activos','SueldoP','Vacantes PA','Reclutamiento']
titl=['Empresa','CLASIFICACIÓN','#Empleados Activos','Sueldo promedio','#Vacante promedio anual','Costo de Reclutamiento']
colsdict={i:j for i,j in zip(colsl,titl)}
tablal=df[df.Puesto==puesto]
HBT = 100*tablal['Costo ReclutamientoP'].sum()/tablal['Costo Nomina'].sum()
HB=tablal['%HB'].copy()
tabla=tablal[colsl]
dataup={}
for col,tit in zip(st.columns(6),colsl):
    for row,index in zip(tabla[tit],tabla[tit].index):
        if isinstance(row, float):
            if colsdict[tit] in ['Sueldo promedio','Costo de Reclutamiento']:
                dataup[(tit,index)]=col.text_area(colsdict[tit], str("${:,.2f}".format(float(row))),key=(tit,index)).replace(',','').replace('$','')
            else:
                dataup[(tit,index)]=col.text_area(colsdict[tit], str("{:,.0f}".format(float(row))),key=(tit,index)).replace(',','').replace('$','')
        else:
            dataup[(tit,index)]=col.text_area(colsdict[tit],str(row),key=(tit,index))


for i,j in dataup.items():
    tabla[i[0]][i[1]]=j
tabla['Costo Reclutamiento Total']=tabla['Vacantes PA']*tabla['Reclutamiento']
tabla['Gasto Promedio Total']=tabla['Activos']*tabla['SueldoP']
tabla['Hiring Budget']=[(i/j)*100 if j >0 else 0 for i,j in zip(tabla['Costo Reclutamiento Total'],tabla['Gasto Promedio Total'])]
tablaf=tabla.drop(columns=['Activos','SueldoP','Vacantes PA','Reclutamiento'])
tablaf['Diferencia']=tablaf['Hiring Budget']-HB
tablaf['Diferencia']=[round(i,2) for i in tablaf['Diferencia']]
totales=pd.DataFrame({'Empresa':['Total'],
                      'Costo Reclutamiento Total':[tablaf['Costo Reclutamiento Total'].sum()],
                      'Gasto Promedio Total':[tablaf['Gasto Promedio Total'].sum()],
                      'Hiring Budget':[100*tablaf['Costo Reclutamiento Total'].sum()/tablaf['Gasto Promedio Total'].sum()]
                      })
totales['Diferencia']=totales['Hiring Budget']-HBT
totales['Diferencia']=[round(i,2) for i in totales['Diferencia']]
tablaff=pd.concat([tablaf,totales]).reset_index().drop(columns=['index']).fillna('')
tablaff['Costo Reclutamiento Total']=tablaff['Costo Reclutamiento Total'].map('${:,.2f}'.format)
tablaff['Gasto Promedio Total']=tablaff['Gasto Promedio Total'].map('${:,.2f}'.format)
tablaff['Hiring Budget']=tablaff['Hiring Budget'].map('{:.3f}'.format)
tablaff['Diferencia']=tablaff['Diferencia'].map('{:.3f}'.format)
st.table(tablaff.rename(columns={'Gasto Promedio Total':'Gasto Nomina'}).style.apply(rowStyle, axis=1).applymap(highlight_max,subset='Diferencia') ) 
#st.write(tablaff.index)
