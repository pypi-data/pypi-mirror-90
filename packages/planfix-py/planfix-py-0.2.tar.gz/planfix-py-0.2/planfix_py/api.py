from requests import post
from requests.auth import HTTPBasicAuth


class PlanfixAPI(object):
	account = None
	token = None
	api_key = None 
	
	url = 'https://api.planfix.ru/xml'
	headers = {'Accept': 'application/xml', 'Content-Type': 'application/xml'}

	def __init__(self, account=None, token=None, api_key=None):
		self.account = account
		self.token = token
		self.api_key = api_key

	def _send_request(self, xml):
		response = post(
				self._URL, 
				data=xml.encode('UTF-8'), 
				headers=self._HEADERS, 
				auth=HTTPBasicAuth(
						self._api_key,
						self._token, 
					)
			)

		text = response.text
		return text
