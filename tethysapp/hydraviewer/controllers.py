from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from tethys_sdk.gizmos import MapView, Button, SelectInput, MVView, DatePicker, RangeSlider

import ee
import hydrafloods as hf

import rastersmith as rs

ee.Initialize()

admin_layer = hf.getAdminMap()

# @login_required()
def home(request):
    """
    Controller for the app home page.
    """
    save_button = Button(
        display_text='',
        name='save-button',
        icon='glyphicon glyphicon-floppy-disk',
        style='success',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Save'
        }
    )

    edit_button = Button(
        display_text='',
        name='edit-button',
        icon='glyphicon glyphicon-edit',
        style='warning',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Edit'
        }
    )

    remove_button = Button(
        display_text='',
        name='remove-button',
        icon='glyphicon glyphicon-remove',
        style='danger',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Remove'
        }
    )

    previous_button = Button(
        display_text='Previous',
        name='previous-button',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Previous'
        }
    )

    next_button = Button(
        display_text='Next',
        name='next-button',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Next'
        }
    )

    context = {
        'save_button': save_button,
        'edit_button': edit_button,
        'remove_button': remove_button,
        'previous_button': previous_button,
        'next_button': next_button
    }

    return render(request, 'hydraviewer/home.html', context)

def mapviewer(request):
    """
    Controller for the app home page.
    """

    precip_layer1 = hf.getPrecipMap(accumulation=1)
    precip_layer3 = hf.getPrecipMap(accumulation=3)
    precip_layer7 = hf.getPrecipMap(accumulation=7)

    gr = rs.Grid(region=(92,5.5,109.5,28.5),resolution=100)
    region = ee.Geometry.Rectangle([gr.west,gr.south,gr.east,gr.north])

    historical_layer = hf.getHistoricalMap(region,'2010-01-01','2015-12-31',month=8,algorithm='JRC')


    sentinel1_layer = hf.Sentinel1(gr).getFloodMap('2018-09-01','2018-09-30')


    product_selection = SelectInput(
        # display_text='Select precipitation product:',
        name='product_selection',
        multiple=False,
        options=[('1 Day Accumulation', '1|'+precip_layer1),
                 ('3 Day Accumulation', '2|'+precip_layer3),
                 ('7 Day Accumulation', '3|'+precip_layer7)],
        initial=['1 Day Accumulation'],
        select2_options={'placeholder': 'Select a product',
                         'allowClear': False}
    )


    context = {
        'precip_layer': precip_layer1,
        'historical_layer': historical_layer,
        'sentinel1_layer': sentinel1_layer,
        'admin_layer': admin_layer,
        'product_selection': product_selection,
    }

    return render(request, 'hydraviewer/map.html', context)

def historical(request):
    """
    Controller for the app home page.
    """
    mekongBuffer = ee.FeatureCollection('ft:1LEGeqwlBCAlN61ie5ol24NdUDqB1MgpFR_sJNWQJ');
    mekongRegion = mekongBuffer.geometry();

    region = ee.Geometry.Rectangle([-180,-90,180,90])

    algorithm_selection = SelectInput(
        # display_text='Select Surface Water Algorithm:',
        name='algorithm_selection',
        multiple=False,
        options=[('Surface Water Tool', 'SWT'), ('JRC Tool', 'JRC')],
        initial=['JRC Tool'],
    )

    # Date Picker Options
    date_picker1 = DatePicker(name='date_picker1',
                              # display_text='Start Date',
                              autoclose=True,
                              format='yyyy-mm-dd',
                              start_date='1/1/1990',
                              start_view='decade',
                              today_button=True,
                              initial='2000-01-01')

    # Date Picker Options
    date_picker2 = DatePicker(name='date_picker2',
                              # display_text='End Date',
                              autoclose=True,
                              format='yyyy-mm-dd',
                              start_date='1/1/1990',
                              start_view='decade',
                              today_button=True,
                              initial='2015-12-31')

    month_slider = RangeSlider(display_text='Month',
                      name='month_slider',
                      min=1,
                      max=12,
                      initial=7,
                      step=1)





    view_options = MVView(
        projection='EPSG:4326',
        center=[101.75, 16.50],
        zoom=5,
        maxZoom=18,
        minZoom=2
    )

    water_map = MapView(
        height='100%',
        width='100%',
        controls=['FullScreen',
                  {'MousePosition': {'projection': 'EPSG:4326'}}],
        basemap='OpenSteetMap',
        view=view_options
    )

    update_button = Button(
        display_text='Update Map',
        name='update-button',
        icon='glyphicon glyphicon-refresh',
        style='success',
        attributes={
            'title':'Update Map'
        }
    )

    context = {
        'update_button': update_button,
        'date_picker1': date_picker1,
        'date_picker2': date_picker2,
        'month_slider': month_slider,
        'algorithm_selection': algorithm_selection,
        'water_layer': water_layer,
        'water_map': water_map,
    }

    return render(request, 'hydraviewer/historical.html', context)
