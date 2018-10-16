var map,
    precip_layer,
    precip_source,
    historical_layer,
    historical_source,
    sentinel1_layer,
    sentinel1_source,
    admin_layer,
    admin_source,
    $layers_element,
    precip_on;

$(function() {

  var precipSlider = $('#precip-opacity').slider();
  var historicalSlider = $('#historical-opacity').slider();

  precip_on = 1

  // Get the Open Layers map object from the Tethys MapView
  map = new ol.Map({
      target: 'map',
      layers: [
        new ol.layer.Tile({
          source: new ol.source.OSM()
        })
      ],
      view: new ol.View({
        center: ol.proj.fromLonLat([101.75, 16.50]),
        zoom: 6,
        minZoom:2,
        maxZoom:16,
      })
    });

  $layers_element = $('#layers');
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

  sentinel1_layer = addMapLayer(sentinel1_layer,sentinel1_source,$layers_element.attr('data-sentinel1-url'))
  historical_layer = addMapLayer(historical_layer,historical_source,$layers_element.attr('data-historical-url'))
  precip_layer = addMapLayer(precip_layer,precip_source,$layers_element.attr('data-precip-url'))

  admin_layer = addMapLayer(admin_layer,admin_source,$layers_element.attr('data-admin-url'))


  $('#product_selection').change(function(){
    var prod = $('#product_selection').val();
    var url = prod.split('|')[1]
    precip_source = new ol.source.XYZ({url:url});
    precip_layer.setSource(precip_source)
  }).change();

  $('#precip-opacity').change(function(){
    var opac = parseFloat($('input[id="precip-opacity"]').slider('getValue'))
    precip_layer.setOpacity(opac)
  });

  $('#historical-opacity').change(function(){
    var opac = parseFloat($('input[id="historical-opacity"]').slider('getValue'))
    historical_layer.setOpacity(opac)
  });

  $("#precip-check").on("click",function(){
    if(this.checked){
      precipSlider.slider('enable')
      var opac = parseFloat($('input[id="precip-opacity"]').slider('getValue'))
      precip_layer.setOpacity(opac)
    }
    else{
      precipSlider.slider('disable')
      precip_layer.setOpacity(0)
    }
  });

});

// function to add and update tile layer to map
function addMapLayer(layer,source,url){
  source = new ol.source.XYZ(
    {url:url}
  );
  layer = new ol.layer.Tile(
    {source:source}
  );
  map.addLayer(layer)
  return layer
}
