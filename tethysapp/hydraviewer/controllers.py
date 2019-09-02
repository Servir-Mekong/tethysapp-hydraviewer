from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from tethys_sdk.gizmos import MapView, Button, SelectInput, MVView, DatePicker, RangeSlider, ToggleSwitch

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
    private_key_password='notasecret',
    scopes=ee.oauth.SCOPE + ' https://www.googleapis.com/auth/drive '
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
    isodate = today.strftime('%Y-%m-%d')
    initial_date = '2016-07-14'
    precip_date = isodate

    if request.method == 'GET':
        info = request.GET
    else:
        info = request.POST

    event_content = info.get('text')
    start_date = info.get('sDate')
    sensor = info.get('sensor_txt')
    viewer = info.get('viewer')
    if not start_date:
        start_date = initial_date

    if not sensor:
        sensor = 'viirs'

    if not event_content:
        event_content = ''

    precip_layer1 = geeutils.getPrecipMap(start_date,accumulation=1)
    historical_layer = geeutils.getHistoricalMap(REGION, '2010','2015', '01', '01', climatology=False, algorithm='JRC', wcolor='#00008b')
    flood_layer = geeutils.getfloodMap('sentinel1', start_date, fcolor='#9999ff', shape=REGION)

    date_selection = DatePicker(
        name='date_selection',
        # display_text='Start Date',
        autoclose=True,
        format='yyyy-mm-dd',
        start_view='decade',
        today_button=True,
        initial=start_date
    )
    update_button = Button(
        display_text='Update Water Layer',
        name='update-button',
        icon='glyphicon glyphicon-refresh',
        style='primary',
        classes="btn_custom"
    )

    method_historical_selection = SelectInput(
        name='method_historical_selection',
        multiple=False,
        options=[('Continuous', 'continuous'),
                 ('Seasonal', 'discrete')],
        initial=['Continuous'],
        select2_options={'placeholder': 'Select a mothod',
                         'allowClear': False}
    )

    start_month_selection_historical = DatePicker(
        name='start_month_selection_historical',
        format= 'mm',
        autoclose= True,
        #startDate= new Date('1984'),
        #endDate: new Date('2015'),
        clear_button= True,
        start_view= 'months',
        min_view_mode= 'months',
        initial='01'

    )

    end_month_selection_historical = DatePicker(
        name='end_month_selection_historical',
        format= 'mm',
        autoclose= True,
        #startDate= new Date('1984'),
        #endDate: new Date('2015'),
        clear_button= True,
        start_view= 'months',
        min_view_mode= 'months',
        initial='02'

    )


    start_year_selection_historical = DatePicker(
        name='start_year_selection_historical',
        format= 'yyyy',
        autoclose= True,
        #start_date= '1/1/2015',
        #end_date = '1/1/2016',
        clear_button= True,
        start_view= 'years',
        min_view_mode= 'years',
        initial='2010'
    )

    end_year_selection_historical = DatePicker(
        name='end_year_selection_historical',
        format= 'yyyy',
        autoclose= True,
        #start_date= new Date('2010'),
        #endDate: new Date('2015'),
        clear_button= True,
        start_view= 'years',
        min_view_mode= 'years',
        initial='2015'
    )

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
        options=[
                 ('Sentinel 1', 'sentinel1'),
                 ('VIIRS Downscaled','viirs'),
                 ('ATMS (Comming soon)', 'atms')],
        initial=['Sentinel 1'],
        select2_options={'placeholder': 'Select sensor:',
                         'allowClear': False}
    )

    toggle_switch_historic = ToggleSwitch(
        name='toggle_switch_historic',
        on_style='success',
        off_style='default',
        initial=True,
        size='small'
    )

    toggle_switch_daily = ToggleSwitch(
        name='toggle_switch_daily',
        on_style='success',
        off_style='default',
        initial=True,
        size='small'
    )

    context = {
        'date_selection': date_selection,
        'precip_layer': precip_layer1,
        'historical_layer': historical_layer,
        'flood_layer':flood_layer,
        'admin_layer': ADMIN_LAYER,
        'product_selection': product_selection,
        'cmap_selection': cmap_selection,
        'browse_selection': browse_selection,
        'sensor_selection':sensor_selection,
        'start_month_selection_historical' : start_month_selection_historical,
	    'start_year_selection_historical' : start_year_selection_historical,
        'end_month_selection_historical' : end_month_selection_historical,
	    'end_year_selection_historical' : end_year_selection_historical,
        'method_historical_selection' : method_historical_selection,
        'update_button' : update_button,
        'toggle_switch_historic': toggle_switch_historic,
        'toggle_switch_daily': toggle_switch_daily,
        'event_content': event_content,
        'sensor': sensor,
        'event_date': start_date

    }
    if not viewer:
        return render(request, 'hydraviewer/map.html', context)
    else:
        return render(request, 'hydraviewer/usecase-viewer.html', context)
