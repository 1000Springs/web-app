var max = 100;
var min = 0;

// Start slider
$(function()
{

 $("#slider").rangeSlider({
  formatter:function(val){
         var value = Math.round(val);          
         return value.toString()  + "°C";     
      }});
});



//Highlight filter items
$(function()
{
  $('.filterImage input').change(function()
  {
      if($(this).is(':checked'))
      {      
        $(this).siblings('label').children().animate(
          {
            "opacity": "1"
          }, "fast");
      }
      else
      {
        $(this).siblings('label').children().animate(
          {
            "opacity": "0.6"
          }, "fast");
      }
  });
});



//Setting the preset temperature ranges
function presetTemp(id,low,high)
{
  $(id).click(function()
   {
    $("#slider").rangeSlider("values", low, high);  
   });  
}

//Setting up preset temperature ranges
$(function()
{

presetTemp("#safe",min,35);
presetTemp("#unsafe",35,max);
presetTemp("#hottest",Math.ceil(max*0.90),max);



});

$(function()
{
    $("#minTemp").val(Math.round($("#slider").rangeSlider("values").min));
    $("#maxTemp").val(Math.round($("#slider").rangeSlider("values").max));
  $("#slider").bind("valuesChanged", function(e, data)
  {  
    $("#minTemp").val(Math.round(data.values.min));
    $("#maxTemp").val(Math.round(data.values.max));
  });
});

//Start Map
$(function()
{
   navigator.geolocation.getCurrentPosition(show_map);
   codeLatLng();
   $('img').tooltip();
 });

// function codeLatLng(latLng) 
// {
//     geocoder = new google.maps.Geocoder();
   
//     geocoder.geocode({'latLng': latLng}, function(results, status) {
//    if (status == google.maps.GeocoderStatus.OK) {
//      if (results[5]) 
//      {
//        var cityName = results[5].formatted_address;        

//        $('#myLoc').val($.trim(cityName.split(",")[0]));
//        $('#nearby').val($.trim(cityName.split(",")[0]));
//      }   
//    }
//    else
//    {
//      $('#myLoc').val("Could not find your location");
//    }   
//     });
//   }