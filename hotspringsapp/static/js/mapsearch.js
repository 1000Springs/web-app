var map;
var myLatLng;
function initialize() {


	myLatlng = new google.maps.LatLng(-38.596065,176.263192);

	
	

	
	var mapOptions = 
	{
	center: myLatlng,
	zoom: 6,
	mapTypeId: google.maps.MapTypeId.HYBRID
	};
	
	map = new google.maps.Map(document.getElementById("map_canvas"),mapOptions);


var layer = new google.maps.FusionTablesLayer({
   query:{
      select:'Address',
      from:'1u4uUgYRC0E02kg7w9_q6pOy1vkh7z3Xy7Nmo2VE'
   },
   styles:[
      {
         polygonOptions:{
            fillColor:"#FF0000",
            strokeColor:"#FFFFFF",
            strokeWeight:"int"
         }
      }
   ],
   map:map,
   suppressInfoWindows:true
});
      
 google.maps.event.addListener(layer, 'click', function(e) 
 {

  //alert(e.row['name'].value);
  alert(e.row['NAME'].value);
});

 google.maps.event.addListener(layer, 'mouseover', function(e)
 {

 	alert("awesome");
 });

}

function addMarker(city, lat, lng, site_name, desc, siteID)
{

 var marker = new google.maps.Marker({
     position: new google.maps.LatLng(lat,lng),
     map: map,
     title: site_name,
     id: siteID
  });

 
 
 google.maps.event.addListener(marker, 'click', function() {

  addSelected(marker);
});
  

}

function addSelected(marker)
{

	
	$("#selected").append("<div><p>" + marker.title +  '<button type="button" class="close" onclick="deleteSelected.call(this)">×</button>' + "</p>" + '<input type="hidden" name="sampleSite" value="'+marker.id+'"> </div>');

}

function deleteSelected()
{
	$(this).closest("div").remove();
	
}