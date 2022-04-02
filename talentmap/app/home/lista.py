import utilsm as ut
import pandas as pd
todid=ut.bd[['ID','Function']].drop_duplicates()
lidid=ut.bdl[['ID','Function']].drop_duplicates()
todid['Indice de Competencias'] = [ut.get_it(i) for i in todid.ID]
lidid['Indice de Competencias'] = [ut.get_itl(i) for i in lidid.ID]
todid['Indice de Suceción']=[ut.get_isn(i,'todos') for i in todid.ID]
lidid['Indice de Suceción']=[ut.get_isn(i,'lideres') for i in lidid.ID]
todid['Origen']='Todos'
lidid['Origen']='Lideres'
pd.concat([lidid,todid]).to_csv('BaseIndices.csv',index=False)
