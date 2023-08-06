"""Luchtmeetnet library to get parsed Airquality data from luchtmeetnet.nl."""
import logging
from requests.exceptions import HTTPError
from math import cos, asin, sqrt

import aiohttp

from luchtmeetnet.constants import TIMEOUT

from luchtmeetnet.urls import json_stations_url, json_station_data_url, json_station_lki_data

log = logging.getLogger(__name__)


class LuchtmeetNet:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        self.location = {'latitude': latitude, 'longitude': longitude}

    async def get_station_measurement(self, station):
        data = {}
        url = json_station_lki_data(station)

        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=TIMEOUT)) as client:
            result = await self._fetchdata(client,url)
            if result is not None:
                try:
                    measurements = result['data']
                    if len(measurements) > 0:
                        data = {
                            'LKI' : measurements[0]['value'],
                            'timestamp' : measurements[0]['timestamp_measured'],
                            'test' : 0
                        }
                except Exception as err:
                    log.error(f"An error ocurred: {err}")
        return data


    async def get_nearest_station(self):
        log.info("Finding nearest station")
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=TIMEOUT)) as client:
            stations = await self.__get_stations(client)
            return self.__closest(stations,self.location)



    async def __get_stations(self, client):
        stations = []
        url_stations = json_stations_url(1)
        result = await self._fetchdata(client,url_stations)
        if result is not None:
            try:
                for page in result['pagination']['page_list']:
                    url_station = json_stations_url(page)
                    res = await self._fetchdata(client,url_station)
                    if res is not None:
                        for station in res['data']:
                            station_data_url = json_station_data_url(station['number'])
                            station_result = await self._fetchdata(client,station_data_url)
                            if station_result is not None:
                                element = {'number' : station['number'],
                                           'longitude' : station_result['data']['geometry']['coordinates'][0],
                                           'latitude' :  station_result['data']['geometry']['coordinates'][1],
                                           'location' : station_result['data']['location']
                                }                        
                                stations.append(element)
                                                    
            except Exception as err:
                log.error(f"An error ocurred: {err}")
            return stations

    async def _fetchdata(self, client, url):
        response = None
        try:
            response = await client.get(url)
            response.raise_for_status()
            async with response:
                if response.status == 200:
                    result = await response.json()
                    return result
                else:
                    return None
        except HTTPError as http_err:
            log.error(f"HTTP error occurred: {http_err}")
            return None
        except Exception as err:
            log.error(f"An error ocurred: {err}")
            return None
        finally:
            if response is not None:
                await response.release()        


    def __distance(self, lat1, lon1, lat2, lon2):
        p = 0.017453292519943295
        a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
        distance = 12742 * asin(sqrt(a))
        return distance

    def __closest(self, data, v):
        return min(data, key=lambda p: self.__distance(v['latitude'],v['longitude'],p['latitude'],p['longitude']))
