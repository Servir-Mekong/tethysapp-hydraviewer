import ee
from ee.ee_exception import EEException
from . import geeutils
from . import config
import json
from django.http import JsonResponse
import datetime

try:
    ee.Initialize()
except EEException as e:
    from oauth2client.service_account import ServiceAccountCredentials
    credentials = ServiceAccountCredentials.from_p12_keyfile(
    service_account_email=config.SERVICEACCOUNT,
    filename=config.KEYFILE,
    )
    ee.Initialize(credentials)

region = ee.Geometry.Rectangle(config.BOUNDING_BOX)

def update_historical(request):
    return_obj = {}

    if request.method == 'POST':
        try:
            info = request.POST;
            start = info.get('sDate')
            end = info.get('eDate')
            month = info.get('month')
            algo = info.get('algo')
            climo = bool(int(info.get('climo')))

            water_layer = geeutils.getHistoricalMap(region,start,end,month=month,algorithm=algo,climatology=climo)

            return_obj["url"] = water_layer
            return_obj["success"] = "success"

        except Exception as e:
            return_obj["error"] = "Error Processing Request. Error: "+ str(e)

    return JsonResponse(return_obj)

def get_precipmap(request):
    return_obj = {}

    if request.method == 'POST':
        try:
            info = request.POST;
            start_date = info.get('sDate')
            accum = int(info.get('accum'))
            cmap = info.get('cmap')

            precip_layer = geeutils.getPrecipMap(start_date,accum,cmap_name=cmap)

            return_obj["url"] = precip_layer
            return_obj["success"] = "success"

        except Exception as e:
            return_obj["error"] = "Error Processing Request. Error: "+ str(e)

    return JsonResponse(return_obj)


def get_surfacewatermap(request):
    return_obj = {}

    if request.method == 'POST':
        try:
            info = request.POST;
            start_date = info.get('sDate')
            sensor = info.get('sensor_txt')

            water_layer = geeutils.getfloodMap(sensor,start_date)

            return_obj["url"] = water_layer
            return_obj["success"] = "success"

        except Exception as e:
            return_obj["error"] = "Error Processing Request. Error: "+ str(e)

    return JsonResponse(return_obj)

def download_surfacewatermap(request):
    return_obj = {}

    if request.method == 'POST':
        try:
            info = request.POST;
            start_date = info.get('sDate')
            sensor = info.get('sensor_txt')
            poly = info.get('poly_coordinates')
            download_url  = geeutils.GetDownloadURL(sensor,start_date,poly)

            return_obj["url"] = download_url
            return_obj["success"] = "success"

        except Exception as e:
            return_obj["error"] = "Error Processing Request. Error: "+ str(e)

    return JsonResponse(return_obj)
