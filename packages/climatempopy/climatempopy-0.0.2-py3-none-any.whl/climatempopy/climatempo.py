from .const import *
from  climatempopy import common

class ClimaTempo:    

    def __init__(self, session, climatempo_token, locale_id=None):
        self.session = session
        self.climatempo_token = climatempo_token
        self.locale_id = locale_id
        self.current = None
        self.forecast_72_hours= None
        self.forecast_15_days= None

    async def get_current_weather(self):
        url = API_URL+CURRENT_WEATHER_URL.format(self.locale_id)
        return await self.get_climatempo_object_data(url)

    async def get_72_hours_forecast(self):
        url = API_URL+FORECAST_72_HOURS_URL.format(self.locale_id)
        return await self.get_climatempo_object_data(url)

    async def get_15_days_forecast(self):
        url = API_URL+FORECAST_15_DAYS_URL.format(self.locale_id)
        return await self.get_climatempo_object_data(url)

    async def get_locales(self,city,state=None,country=None):
        url = API_URL+SEARCH_LOCALE_URL.format(self.locale_id)
        params = {}
        params["name"]=city.upper()
        if state:
            params["state"]=state.upper()
        if country:
            params["country"]=country.upper()
        return await self.get_climatempo_object_data(url,params)

    async def get_climatempo_object_data(self, url, params=None):
        if not params:
            params = {}
        params[TOKEN_PARAMETER_STR]=self.climatempo_token
        current = await common.async_http_request(self.session,url,params)
        return common.json_to_object(current) 
    
    async def update_current_weather(self):
        self.current = await self.get_current_weather()

    async def update_72_hours_forecast (self):
        self.forecast_72_hours = await self.get_72_hours_forecast()
    
    async def update_15_days_forecast (self):
        self.forecast_15_days = await self.get_15_days_forecast()
    
    async def set_locale_id_from_coords(self,latitude,longitude):
        self.locale_id= await self.get_locale_from_coords(self,latitude,longitude)

    async def get_locale_from_coords(self,latitude,longitude):
        location=common.get_address("climatempopy_lib",coords='{},{}'.format(latitude,longitude))
        return await self.get_locales(location.address.city,common.get_state_abbreviation(location.address.state),location.address.country_code)