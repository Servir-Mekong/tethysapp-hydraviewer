import ee
import hydrafloods as hf
import json
from django.http import JsonResponse
import datetime

ee.Initialize()

region = ee.Geometry.Rectangle([-180,-90,180,90])

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

            water_layer = hf.getHistoricalMap(region,start,end,month=month,algorithm=algo,climatology=climo)

            return_obj["url"] = water_layer
            return_obj["success"] = "success"

        except Exception as e:
            return_obj["error"] = "Error Processing Request. Error: "+ str(e)

    return JsonResponse(return_obj)
