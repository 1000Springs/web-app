
var myLatlng;
var markersArray = [];

function addInfoWindowMarker(city, lat, lng, site_name, desc, map)
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


function setupMap(mapElementId) 
{
  var mapOptions = 
  {
      center: new google.maps.LatLng(-37.8256,175.2954),
    zoom: 6,
    mapTypeId: google.maps.MapTypeId.ROADMAP 
  };

  navigator.geolocation.getCurrentPosition(showUserLocation);
  return new google.maps.Map(document.getElementById(mapElementId),mapOptions);

}

function showUserLocation(position) 
{
  var latitude = position.coords.latitude;
  var longitude = position.coords.longitude;
  myLatlng = new google.maps.LatLng(latitude,longitude); 
}

function addNewMarker(markerPosition,markerIcon,mapElement)
{

  var marker = new google.maps.Marker({
     position: markerPosition,
     map: mapElement,
     icon: markerIcon
  });
  markersArray.push(marker);
  return marker;
}

function clearMarkers()
{
  if (markersArray) 
  {
    for (i in markersArray) 
    {
      markersArray[i].setMap(null);
    }
  }
}

function resize(marker)
{
  google.maps.event.trigger(modalMap, 'resize');   
  modalMap.setCenter(marker.position);
}


	  
