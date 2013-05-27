var map;
var searchMap;
var myLatlng;
var geocoder;

var markersArray = [];

function initialize() {

	navigator.geolocation.getCurrentPosition(show_map);

	var mapOptions = 
	{
  center: new google.maps.LatLng(-37.8256,175.2954),
	zoom: 6,
	mapTypeId: google.maps.MapTypeId.HYBRID
	};
	
	map = new google.maps.Map(document.getElementById("map_canvas"),mapOptions);
	searchMap = new google.maps.Map(document.getElementById("show_map"),mapOptions);
	
  
 $("#expand").toggle(function () {
    $("#map_canvas").animate({
        "height": "500px"
    }, "slow", function () {
		//Resizes map once animation has finished
        google.maps.event.trigger(map, 'resize');		
    });
    $("#expand").prop('value', 'Reduce Map');
}, function () {
    $("#map_canvas").animate({
        "height": "200px"
    }, "slow", function () {
        google.maps.event.trigger(map, 'resize');
    });
    $("#expand").prop('value', 'Enlarge Map');
    google.maps.event.trigger(map, 'resize');
});

}

function initalizeSampleSite()
{
  var mapOptions = 
  {
  center: new google.maps.LatLng(-37.8256,175.2954),
  zoom: 6,
  mapTypeId: google.maps.MapTypeId.HYBRID
  };
  
  navigator.geolocation.getCurrentPosition(show_map);
  searchMap = new google.maps.Map(document.getElementById("show_map"),mapOptions);
}

function addMarker(city, lat, lng, site_name, desc)
{

 var contentString = '<div id="content" style="height:100px">'+
    '<h5 id="firstHeading" class="firstHeading">'+site_name+'</h5>'+
    '<div id="bodyContent">'+
    '<p class="muted">'+city+'</p>'+
    '</div>'+
    '</div>';	

var infoWindow = new google.maps.InfoWindow({
    content: contentString
});

 var marker = new google.maps.Marker({
     position: new google.maps.LatLng(lat,lng),
     map: map,
     title: city
  });
 
 google.maps.event.addListener(marker, 'click', function() {
  infoWindow.open(map,marker);
});
  

}

function show_map(position) 
{
  var latitude = position.coords.latitude;
  var longitude = position.coords.longitude;
  myLatlng = new google.maps.LatLng(latitude,longitude);

  var marker = new google.maps.Marker({
     position: myLatlng,
     map: searchMap,
     icon: "http://www.google.com/mapfiles/arrow.png"
  });
  codeLatLng(myLatlng);

  
}

function codeLatLng(latLng) 
{
    geocoder = new google.maps.Geocoder();
   
    geocoder.geocode({'latLng': latLng}, function(results, status) {
		if (status == google.maps.GeocoderStatus.OK) {
			if (results[5]) 
			{
				var cityName = results[5].formatted_address;				

				$('#myLoc').val($.trim(cityName.split(",")[0]));
				$('#nearby').val($.trim(cityName.split(",")[0]));
			}		
		}
		else
		{
			$('#myLoc').val("Could not find your location");
		}	  
    });
  }

function modalInit()
{
  clearMarkers();
  var position = $(this).closest("div").children("input")[0].value.split(",");

  var position = new google.maps.LatLng(position[0],position[1]);

  var feature_name = $(this).closest('tr').find('.feature_name').html();

  $(".modal-footer").html('<p> View in <a href="http://maps.google.co.nz/maps?t=h&q=loc:'+position.lat()+','+position.lng()+'&z=10"> google maps </a> </p>');
 
  $("#myModalLabel").html(feature_name);

  var marker = addNewMarker(position,"http://maps.google.com/mapfiles/ms/icons/blue-dot.png");
  markersArray.push(marker);

  window.setTimeout(function() {
  resize(marker);
}, 1000, true);
  searchMap.setCenter(marker.position);
  
}

function addNewMarker(markerPosition,markerIcon)
{

  var marker = new google.maps.Marker({
     position: markerPosition,
     map: searchMap,
     icon: markerIcon
  });
  markersArray.push(marker);
  return marker;
}

function clearMarkers()
{
   if (markersArray) {
    for (i in markersArray) {
      markersArray[i].setMap(null);
    }
  }
}

function resize(marker)
{
  google.maps.event.trigger(searchMap, 'resize');   
  searchMap.setCenter(marker.position);
}


	  
