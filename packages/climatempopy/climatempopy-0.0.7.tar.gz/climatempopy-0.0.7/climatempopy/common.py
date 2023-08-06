from geopy.geocoders import Nominatim
from types import SimpleNamespace
from unidecode import unidecode
import json

states_abbreviation = {'ACRE':'AC',
'ALAGOAS':'AL',
'AMAZONAS':'AM',
'AMAPA':'AP',
'BAHIA':'BA',
'CEARA':'CE',
'DISTRITO FEDERAL':'DF',
'ESPÍRITO SANTO':'ES',
'GOIAS':'GO',
'MARANHAO':'MA',
'MINAS GERAIS':'MG',
'MATO GROSSO DO SUL':'MS',
'MATO GROSSO':'MT',
'PARA':'PA',
'PARAIBA':'PB',
'PERNAMBUCO':'PE',
'PIAUI':'PI',
'PARANA':'PR',
'RIO DE JANEIRO':'RJ',
'RIO GRANDE DO NORTE':'RN',
'RONDONIA':'RO',
'RORAIMA':'RR',
'RIO GRANDE DO SUL':'RS',
'SANTA CATARINA':'SC',
'SERGIPE':'SE',
'SAO PAULO':'SP',
'TOCANTIS':'TO'}

def get_state_abbreviation(state_name):
    return states_abbreviation[unidecode(state_name).upper()]
    
def get_address(user_agent,coords):
    geolocator = Nominatim(user_agent=user_agent)
    return json_to_object(json.dumps(geolocator.reverse(coords).raw))

def json_to_object(data):
    return json.loads(data, object_hook=lambda d: SimpleNamespace(**d))

async def async_http_request(session, url, params=None):
    async with session.get(url, params=params) as res:
        res.raise_for_status()
        current = await res.text()
    return current