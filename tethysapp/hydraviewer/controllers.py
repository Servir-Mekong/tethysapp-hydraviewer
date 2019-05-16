from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from tethys_sdk.gizmos import MapView, Button, SelectInput, MVView, DatePicker, RangeSlider

import ee
from ee.ee_exception import EEException
import datetime

from . import config
from . import geeutils

WC = ee.ImageCollection(config.WATERCOLLECTION)
REGION = ee.Geometry.Rectangle(config.BOUNDING_BOX)
ADMIN_LAYER = geeutils.getAdminMap(REGION)

try:
    ee.Initialize()
except EEException as e:
    from oauth2client.service_account import ServiceAccountCredentials
    credentials = ServiceAccountCredentials.from_p12_keyfile(
    service_account_email=config.SERVICEACCOUNT,
    filename=config.KEYFILE,
    )
    ee.Initialize(credentials)


# @login_required()
def home(request):
    """
    Controller for the app home page.
    """

    context = {

    }

    return render(request, 'hydraviewer/home.html', context)

def usecases(request):
    """
    Controller for the app home page.
    """

    context = {

    }

    return render(request, 'hydraviewer/usecases.html', context)

def mapviewer(request):
    """
    Controller for the app home page.
    """

    today = datetime.datetime.now()
    thisdate = today-datetime.timedelta(2)
    isodate = thisdate.strftime('%Y-%m-%d')

    precip_layer1 = geeutils.getPrecipMap(isodate,accumulation=1)

    date_selection = DatePicker(
        name='date_selection',
        # display_text='Start Date',
        autoclose=True,
        format='yyyy-mm-dd',
        start_view='decade',
        today_button=True,
        initial=isodate
    )

    historical_layer = geeutils.getHistoricalMap(REGION,'2010-01-01','2015-12-31',month=8,algorithm='JRC')

    image = ee.Image(WC.filter(ee.Filter.eq('sensor','sentinel1')).first())

    product_selection = SelectInput(
        # display_text='Select precipitation product:',
        name='product_selection',
        multiple=False,
        options=[('1 Day Accumulation', '1|0'),
                 ('3 Day Accumulation', '3|0'),
                 ('7 Day Accumulation', '7|0')],
        initial=['1 Day Accumulation'],
        select2_options={'placeholder': 'Select a product',
                         'allowClear': False}
    )

    cmap_selection = SelectInput(
        # display_text='Select precipitation product:',
        name='cmap_selection',
        multiple=False,
        options=[('nipy_spectral', 'nipy_spectral'),
                 ('gist_ncar', 'gist_ncar'),
                 ('cubehelix', 'cubehelix')],
        initial=['nipy_spectral'],
        select2_options={'placeholder': 'Select a product',
                         'allowClear': False}
    )


    browse_selection = SelectInput(
        # display_text='Select precipitation product:',
        name='browse_selection',
        multiple=False,
        options=[('VIIRS NRT TRUE COLOR', '1|VIIRS_SNPP_CorrectedReflectance_TrueColor'),
                 ('VIIRS NRT NATURAL COLOR', '2|VIIRS_SNPP_CorrectedReflectance_BandsM11-I2-I1'),
                 ('MODIS AQUA TRUE COLOR', '3|MODIS_Aqua_CorrectedReflectance_TrueColor'),
                 ('MODIS AQUA NATURAL COLOR', '4|MODIS_Aqua_CorrectedReflectance_Bands721'),
                 ('MODIS TERRA TRUE COLOR', '5|MODIS_Terra_CorrectedReflectance_TrueColor'),
                 ('MODIS TERRA NATURAL COLOR', '5|MODIS_Terra_CorrectedReflectance_Bands721')],
        initial=['VIIRS NRT NATURAL COLOR'],
        select2_options={'placeholder': 'Select browse imagery:',
                         'allowClear': False}
    )

    sensor_selection = SelectInput(
        # display_text='Select precipitation product:',
        name='sensor_selection',
        multiple=False,
        options=[ ('select sensor', 'none'),
                 ('Sentinel 1', 'sentinel1'),
                 ('ATMS', 'atms'),
                 ('VIIRS Downscaled','viirs')],
        initial=['select sensor'],
        select2_options={'placeholder': 'Select sensor:',
                         'allowClear': False}
    )

    context = {
        'date_selection': date_selection,
        'precip_layer': precip_layer1,
        'historical_layer': historical_layer,
        'admin_layer': ADMIN_LAYER,
        'product_selection': product_selection,
        'cmap_selection': cmap_selection,
        'browse_selection': browse_selection,
        'sensor_selection':sensor_selection,
    }

    return render(request, 'hydraviewer/map.html', context)
