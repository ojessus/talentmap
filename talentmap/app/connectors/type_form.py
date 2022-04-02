from decouple import config
import requests as rq
class TYPE_FORM():
	def __init__(self):
		self.acces_token=config('TYPE_FORM_TOKEN')
		self.url_api=config('TYPE_FORM_URL')
	def tfquery(self,ruta,var,tipo='get'):
		url = self.url_api + ruta
		header={'Authorization':'Bearer ' + self.acces_token}
		if tipo == 'get':
			rs=rq.get(url,params=var,headers=header)
		elif tipo=='post':
			rs=rq.post(url,data=var,headers=header)
		else:
			raise Exception('Tipo de request no soportada')
		if rs.status_code==200:
			return {'status_code':200,'data':rs.json(),'message':'OK'}	
		return {'status_code':rs.status_code,'data':{},'message':'Error in request'}
	
		
	
