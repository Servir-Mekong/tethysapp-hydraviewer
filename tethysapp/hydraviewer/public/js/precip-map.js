var map;
var precip_layer;
var precip_source;

$(function() {
  // Get the Open Layers map object from the Tethys MapView
  map = TETHYS_MAP_VIEW.getMap();

  var $layers_element = $('#layers');
  var $update_element = $('#update_button');

  var base_map = new ol.layer.Tile({
            crossOrigin: 'anonymous',
            source: new ol.source.XYZ({
                // attributions: [attribution],
                url: 'https://services.arcgisonline.com/ArcGIS/rest/services/Canvas/' +
                'World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}'
            })
        });

  map.removeLayer(0)
  map.addLayer(base_map);

  //precip_layer = $layers_element.attr('data-precip-url');

  precip_source = new ol.source.XYZ();
  precip_layer = new ol.layer.Tile(
    {
      source:precip_source
    }
  );

  map.addLayer(precip_layer)


  $('#product_selection').change(function(){
    var prod = $('#product_selection').val();
    var url = prod.split('|')[1]
    precip_source = new ol.source.XYZ({url:url});
    precip_layer.setSource(precip_source)
  }).change();

});

function addPrecip(url){

  map.removeLayer(1)

  var precip_layer = new ol.layer.Tile({
            source: new ol.source.XYZ({
                url: url
            })
        });
  map.addLayer(precip_layer)
  return
}
