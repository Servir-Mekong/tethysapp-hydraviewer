from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from tethys_sdk.gizmos import MapView, Button, SelectInput, MVLayer, MVView

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

def precip(request):
    """
    Controller for the app home page.
    """

    product_selection = SelectInput(
        display_text='Select precipitation product:',
        name='product_selection',
        multiple=False,
        options=[('1 Day Accumulation', '1'), ('3 Day Accumulation', '2'), ('7 Day Accumulation', '3')],
        initial=['1 Day Accumulation'],
        select2_options={'placeholder': 'Select a product',
                         'allowClear': False}
    )

    # Create a Map View Layer
    precip_layer = MVLayer(
        source='SERVIR Global',
        options={'url': 'https://gis1.servirglobal.net/arcgis/rest/services/Global/IMERG_Accumulations/MapServer/layers',
               'params': {'LAYERS': '0'},
               # 'serverType': 'TileArcGISRest',
               },
        legend_title='IMERG'
    )

    view_options = MVView(
        projection='EPSG:4326',
        center=[101.75, 16.50],
        zoom=5,
        maxZoom=18,
        minZoom=2
    )

    precip_map = MapView(
        height='100%',
        width='100%',
        controls=['FullScreen',
                  {'MousePosition': {'projection': 'EPSG:4326'}}],
        layers=[precip_layer],
        basemap='OpenSteetMap',
        view=view_options
    )

    context = {
        'precip_map': precip_map,
        'product_selection': product_selection,
    }

    return render(request, 'hydraviewer/precip.html', context)
