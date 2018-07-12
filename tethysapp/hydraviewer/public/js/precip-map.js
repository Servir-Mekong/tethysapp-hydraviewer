$(function() {
  // Get the Open Layers map object from the Tethys MapView
  var map = TETHYS_MAP_VIEW.getMap();

  var base_map = new ol.layer.Tile({
            crossOrigin: 'anonymous',
            source: new ol.source.XYZ({
                // attributions: [attribution],
                url: 'https://services.arcgisonline.com/ArcGIS/rest/services/Canvas/' +
                'World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}'
            })
        });

  map.getLayers().item(0).setVisible(false);
  map.addLayer(base_map);

  var url = 'https://gis1.servirglobal.net/arcgis/rest/services/'+
            'Global/IMERG_Accumulations/MapServer/WMSServer';
  var layer = '6';

  var precip_layer = new ol.layer.Tile ({
            source: new ol.source.TileWMS({
                id:'IMERG',
                // attributions: [attribution],
                url: url,
                params:{'LAYER':layer,'TILED':true}
            })
        });

  // // Add the overlay to the map
  map.addLayer(precip_layer)

  return
});
