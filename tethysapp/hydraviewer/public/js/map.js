var map,
    viirs_layer,
    viirs_source,
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

var today = new Date().toISOString().slice(0, 10)

$(function() {

  var browseSlider = $('#browse-opacity').slider();
  var precipSlider = $('#precip-opacity').slider();
  var historicalSlider = $('#historical-opacity').slider();
  var sentinel1Slider = $('#sentinel1-opacity').slider();


  // Get the Open Layers map object from the Tethys MapView
  map = new ol.Map({
      target: 'map',
      layers: [
        new ol.layer.Tile({
          source: new ol.source.OSM()
        })
      ],
      view: new ol.View({
        projection: 'EPSG:4326',
        center: [101.75, 16.50],//ol.proj.fromLonLat([101.75, 16.50]),
        zoom: 6,
        minZoom:2,
        maxZoom:16,
      })
    });

  $layers_element = $('#layers');
  var $update_element = $('#update_button');

  var viirs_product = "VIIRS_SNPP_CorrectedReflectance_TrueColor"

  viirs_layer = addGibsLayer(viirs_layer,viirs_source,viirs_product,today)


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

  $('#browse-opacity').change(function(){
    var opac = parseFloat($('input[id="browse-opacity"]').slider('getValue'))
    viirs_layer.setOpacity(opac)
  });

  $('#precip-opacity').change(function(){
    var opac = parseFloat($('input[id="precip-opacity"]').slider('getValue'))
    precip_layer.setOpacity(opac)
  });

  $('#historical-opacity').change(function(){
    var opac = parseFloat($('input[id="historical-opacity"]').slider('getValue'))
    historical_layer.setOpacity(opac)
  });

  $('#sentinel1-opacity').change(function(){
    var opac = parseFloat($('input[id="sentinel1-opacity"]').slider('getValue'))
    sentinel1_layer.setOpacity(opac)
  });

  $("#browse-check").on("click",function(){
    if(this.checked){
      browseSlider.slider('enable')
      var opac = parseFloat($('input[id="browse-opacity"]').slider('getValue'))
      viirs_layer.setOpacity(opac)
    }
    else{
      browseSlider.slider('disable')
      viirs_layer.setOpacity(0)
    }
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

  $("#historical-check").on("click",function(){
    if(this.checked){
      historicalSlider.slider('enable')
      var opac = parseFloat($('input[id="historical-opacity"]').slider('getValue'))
      historical_layer.setOpacity(opac)
    }
    else{
      historicalSlider.slider('disable')
      historical_layer.setOpacity(0)
    }
  });

  $("#sentinel1-check").on("click",function(){
    if(this.checked){
      sentinel1Slider.slider('enable')
      var opac = parseFloat($('input[id="sentinel1-opacity"]').slider('getValue'))
      sentinel1_layer.setOpacity(opac)
    }
    else{
      sentinel1Slider.slider('disable')
      sentinel1_layer.setOpacity(0)
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

function addGibsLayer(layer,source,product,date){
  var source = new ol.source.WMTS({
    url: 'https://gibs-{a-c}.earthdata.nasa.gov/wmts/epsg4326/best/wmts.cgi?TIME='+date,
    layer: product,
    format: 'image/jpeg',
    matrixSet: 'EPSG4326_250m',
    tileGrid: new ol.tilegrid.WMTS({
      origin: [-180, 90],
      resolutions: [
        0.5625,
        0.28125,
        0.140625,
        0.0703125,
        0.03515625,
        0.017578125,
        0.0087890625,
        0.00439453125,
        0.002197265625
      ],
      matrixIds: [0, 1, 2, 3, 4, 5, 6, 7, 8],
      tileSize: 512
    })
  });

  var layer = new ol.layer.Tile({
    source: source,
    extent: [-180, -90, 180, 90]
  });

  map.addLayer(layer)
  return layer
}
