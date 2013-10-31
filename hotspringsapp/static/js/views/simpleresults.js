var mainMap;
var modalMap;
var markersArray = [];

function initializeMaps() 
{

	mainMap = setupMap("map_canvas");
	modalMap = setupMap("show_map");
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



function modalInit()
{
  clearMarkers();
  var position = $(this).closest("div").children("input")[0].value.split(",");

  var springPosition = new google.maps.LatLng(position[0],position[1]);

  var feature_name = $(this).closest('tr').find('.feature_name').html();

  var locationMarker = addNewMarker(myLatlng,"http://www.google.com/mapfiles/arrow.png",modalMap); 

  markersArray.push(locationMarker);

  $(".modal-footer").html('<p> View in <a href="http://maps.google.co.nz/maps?t=h&q=loc:'+springPosition.lat()+','+springPosition.lng()+'&z=10"> google maps </a> </p>');
 
  $("#myModalLabel").html(feature_name);

  var marker = addNewMarker(springPosition,"http://maps.google.com/mapfiles/ms/icons/blue-dot.png",modalMap);

  markersArray.push(marker);
  

  window.setTimeout(function() {
  resize(marker);
}, 1000, true);
  modalMap.setCenter(marker.position);
  
}

$(function(){
	var expanded = false;
	$("#expandMap").click(function() 
	{
		if(expanded === false)
		{
			expanded = true;
			$("#map_canvas").css("height","500px");
			$("#map_canvas").css("width","760px");
			google.maps.event.trigger(mainMap, 'resize'); 
			mainMap.panTo(new google.maps.LatLng(-37.8256, 175.2954));
			$(this).attr("value", "Shrink Map");
			$("#chart_div").hide();
		}
		else
		{
			expanded = false;
			$("#map_canvas").css("height","233px");
			$("#map_canvas").css("width","100%");
			google.maps.event.trigger(mainMap, 'resize'); 
			mainMap.panTo(new google.maps.LatLng(-37.8256, 175.2954));
			$(this).attr("value", "Enlarge Map");
			$("#chart_div").show();
		}
	}); 

	
});