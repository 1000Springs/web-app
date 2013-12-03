
var myLatlng;
var currentInfoWindow = null;


function addInfoWindowMarker(city, lat, lng, site_name, desc, map,url)
{
    var link = "";
    if(url !== null)
    {
      link = '<a href='+url + '> More Details </a>'
    }

   

 var contentString = '<div id="content" style="height:100px">'+
    '<h5 id="firstHeading" class="firstHeading">'+site_name+'</h5>'+
    '<div id="bodyContent">'+
    '<p class="muted">'+city+'</p>' +   
    link + 
    '</div>'+
    '</div> '; 

var infoWindow = new google.maps.InfoWindow({
    content: contentString
});

 var marker = addNewMarker(new google.maps.LatLng(lat,lng),null,map);
 marker.infoWindow = infoWindow;

 map.setCenter(marker.position);

 
 google.maps.event.addListener(marker, 'click', function() {

if(currentInfoWindow !== null)
    {
       currentInfoWindow.close();
       currentInfoWindow = null;    
    }
    
  infoWindow.open(map,marker);
  currentInfoWindow = marker.infoWindow;


   
}); 

}



function addNewMarker(markerPosition,icon,mapElement)
{

  var marker = new google.maps.Marker({
     position: markerPosition,
     map: mapElement,
     icon: icon
  });

  return marker;
}



function setupMap(mapElementId) 
{
  var mapOptions = 
  {
      center: new google.maps.LatLng(-38.633098,176.112213),
    zoom: 7,
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




function resize(marker)
{
  google.maps.event.trigger(modalMap, 'resize');   
  modalMap.setCenter(marker.position);
}


	  
