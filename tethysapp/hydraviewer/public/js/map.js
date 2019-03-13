var map,
    browse_layer,
    precip_layer,
    historical_layer,
    sentinel1_layer,
    admin_layer,
    flood_layer,
    drawing_polygon,
    $layers_element;

$(function() {

  var today = new Date()
  console.log(today)

  if (today.getUTCHours() < 12) {
    today.setDate(today.getDate() - 1);
  }
  var dateStr = today.toISOString().slice(0, 10)

  var browseSlider = $('#browse-opacity').slider();
  var precipSlider = $('#precip-opacity').slider();
  var historicalSlider = $('#historical-opacity').slider();
  var sentinel1Slider = $('#sentinel1-opacity').slider();
  var floodSlider = $('#flood-opacity').slider();
  var floodSlider1 = $('#flood1-opacity').slider();

  map = L.map('map',{
    center: [16.50,101.75],
    zoom: 6,
    minZoom:2,
    maxZoom: 16,
    maxBounds: [
     [-120, -220],
     [120, 220]
   ],
 });

// Initialise the FeatureGroup to store editable layers
var editableLayers = new L.FeatureGroup();
map.addLayer(editableLayers);

var drawPluginOptions = {
  draw: {
    polygon: {
      allowIntersection: false, // Restricts shapes to simple polygons
      drawError: {
        color: '#e1e100', // Color the shape will turn when intersects
        message: '<strong>Oh snap!<strong> you can\'t draw that!' // Message that will show when intersect
      },
      shapeOptions: {
        color: '#97009c'
      }
    },
    // disable toolbar item by setting it to false
    polyline: false,
    circle: false, // Turns off this drawing tool
    circlemarker: false,
    rectangle: true,
    marker: false,
    },
  edit: {
    featureGroup: editableLayers, //REQUIRED!!
    remove: false
  }
};

// Initialise the draw control and pass it the FeatureGroup of editable layers
var drawControl = new L.Control.Draw(drawPluginOptions);
map.addControl(drawControl);

var editableLayers = new L.FeatureGroup();
map.addLayer(editableLayers);

map.on('draw:created', function(e) {
  editableLayers.clearLayers();
  var type = e.layerType,
    layer = e.layer;
   
  if (type === 'marker') {
    layer.bindPopup('A popup!');
  }
  userPolygon = layer.toGeoJSON();
  drawing_polygon = JSON.stringify(userPolygon.geometry.coordinates[0]);
 
 
  editableLayers.addLayer(layer);
});

  var positron = L.tileLayer('http://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}.png', {
        attribution: '©OpenStreetMap, ©CartoDB'
      }).addTo(map);

  $layers_element = $('#layers');
  var $update_element = $('#update_button');
  var viirs_product = "VIIRS_SNPP_CorrectedReflectance_BandsM11-I2-I1"

  browse_layer = addGibsLayer(browse_layer,viirs_product,dateStr)


  //sentinel1_layer = addMapLayer(sentinel1_layer,$layers_element.attr('data-sentinel1-url'))
  flood_layer = addMapLayer(flood_layer,$layers_element.attr('data-flood-url'))
  historical_layer = addMapLayer(historical_layer,$layers_element.attr('data-historical-url'))
  precip_layer = addMapLayer(precip_layer,$layers_element.attr('data-precip-url'))
  admin_layer = addMapLayer(admin_layer,$layers_element.attr('data-admin-url'))


  $('#product_selection').change(function(){
    var prod = $('#product_selection').val();
    var url = prod.split('|')[1]
    precip_layer.setUrl(url)
  });

  $('#sensor_selection').change(function(){
    var selected_date = $('#selected_date').val();
    var sensor_val = $('#sensor_selection').val();

    var xhr = ajax_update_database('get_surfacewatermap',{'sDate':selected_date,'sensor_txt':sensor_val},"layers");
    xhr.done(function(data) {
        if("success" in data) {
          flood_layer.setUrl(data.url)
        }else{
          alert('Opps, there was a problem processing the request. Please see the following error: '+data.error);
        }
    });
  });

  $("#btn_download").on("click",function(){
 if(drawing_polygon === undefined){
  alert("Please draw a polygon");
  }else{
     var selected_date = $('#selected_date').val();
     var sensor_val = $('#sensor_selection').val();
     var xhr = ajax_update_database('download_surfacewatermap',{'sDate':selected_date,'sensor_txt':sensor_val,'poly_coordinates': drawing_polygon},"json");
    xhr.done(function(data) {
        if("success" in data) {
          //alert('Download URL: \n'+ data.url)
          window.open(data.url, '_blank');
        }else{
          alert('Opps, there was a problem processing the request. Please see the following error: '+data.error);
        }
    });
}
  });

  $('#browse_selection').change(function(){
    var prod = $('#browse_selection').val();
    var id = prod.split('|')[1]
    var template =
      '//gibs-{s}.earthdata.nasa.gov/wmts/epsg3857/best/' +
      id + '/default/{time}/{tileMatrixSet}/{z}/{y}/{x}.jpg'
    browse_layer.setUrl(template)
  });

  $('#browse-opacity').change(function(){
    var opac = parseFloat($('input[id="browse-opacity"]').slider('getValue'))
    browse_layer.setOpacity(opac)
  });

  $('#precip-opacity').change(function(){
    var opac = parseFloat($('input[id="precip-opacity"]').slider('getValue'))
    precip_layer.setOpacity(opac)
  });

  $('#historical-opacity').change(function(){
    var opac = parseFloat($('input[id="historical-opacity"]').slider('getValue'))
    historical_layer.setOpacity(opac)
  });

  $('#flood1-opacity').change(function(){
    var opac = parseFloat($('input[id="flood1-opacity"]').slider('getValue'))
    flood_layer.setOpacity(opac)
  });

  $("#browse-check").on("click",function(){
    if(this.checked){
      browseSlider.slider('enable')
      var opac = parseFloat($('input[id="browse-opacity"]').slider('getValue'))
      browse_layer.setOpacity(opac)
    }
    else{
      browseSlider.slider('disable')
      browse_layer.setOpacity(0)
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

$("#flood-check").on("click",function(){
    if(this.checked){
      floodSlider1.slider('enable')
      var opac = parseFloat($('input[id="flood1-opacity"]').slider('getValue'))
      flood_layer.setOpacity(opac)
    }
    else{
      floodSlider1.slider('disable')
      flood_layer.setOpacity(0)
    }
  });

$("#download_flood-check").on("click",function(){
    if(this.checked ){
      $("#btn_download").removeAttr('disabled');
    }
    else{
      $("#btn_download").attr('disabled','disabled');
    }
  });
// end of init function
});

// function to add and update tile layer to map
function addMapLayer(layer,url){
  layer = L.tileLayer(url,{attribution:
    '<a href="https://earthengine.google.com" target="_">' +
    'Google Earth Engine</a>;'}).addTo(map);
  return layer
}

function addGibsLayer(layer,product,date){
  var template =
    '//gibs-{s}.earthdata.nasa.gov/wmts/epsg3857/best/' +
    '{layer}/default/{time}/{tileMatrixSet}/{z}/{y}/{x}.jpg';

  layer = L.tileLayer(template, {
    layer: product,
    tileMatrixSet: 'GoogleMapsCompatible_Level9',
    maxZoom: 9,
    time: date,
    tileSize: 256,
    subdomains: 'abc',
    noWrap: true,
    continuousWorld: true,
    // Prevent Leaflet from retrieving non-existent tiles on the
    // borders.
    bounds: [
      [-85.0511287776, -179.999999975],
      [85.0511287776, 179.999999975]
    ],
    attribution:
      '<a href="https://wiki.earthdata.nasa.gov/display/GIBS" target="_">' +
      'NASA EOSDIS GIBS</a>;'
  });

  map.addLayer(layer);

  return layer
}

/*
* Workaround for 1px lines appearing in some browsers due to fractional transforms
* and resulting anti-aliasing.
* https://github.com/Leaflet/Leaflet/issues/3575
*/
// (function () {
//   var originalInitTile = L.GridLayer.prototype._initTile;
//   L.GridLayer.include({
//     _initTile: function (tile) {
//       originalInitTile.call(this, tile);
//
//       var tileSize = this.getTileSize();
//
//       tile.style.width = tileSize.x + 1 + 'px';
//       tile.style.height = tileSize.y + 1 + 'px';
//     }
//   });
// })();
