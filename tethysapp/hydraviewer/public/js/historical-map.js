var map;
var water_layer;
var water_source;

$(function() {

  // With JQuery
  $('#slider1').slider({
  	formatter: function(value) {
  		return 'Current value: ' + value;
  	}
  });

  // Get the Open Layers map object from the Tethys MapView
  var map = TETHYS_MAP_VIEW.getMap();
  var $layers_element = $('#layers');

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

  water_url = $layers_element.attr('data-water-url');

  water_source = new ol.source.XYZ({url:water_url});
  water_layer = new ol.layer.Tile(
    {
      source:water_source
    }
  );

  map.addLayer(water_layer)

  $('[name="update-button"]').on('click',function() {

    var start = $('#date_picker1').val()
    var end = $('#date_picker2').val()
    var mon = $('#slider1').val()
    var algo = $('#algorithm_selection').val()

    console.log(start,end,mon,algo)
    var xhr = ajax_update_database('update_historical',{'sDate':start,'eDate':end,'month':mon,'algo':algo});
    xhr.done(function(data) {
        if("success" in data) {
          console.log(data)
          water_source = new ol.source.XYZ({url:data.url});
          water_layer.setSource(water_source)

        }else{
            alert('Error processing the request.'+data.error);
        }
    });
  });


  return
});
