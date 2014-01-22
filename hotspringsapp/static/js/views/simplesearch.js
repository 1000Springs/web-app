// Start slider
var minTemp = 0;
var maxTemp = 100;

var minCond = 0;
var maxCond = 12000;

var minTurb = 0;
var maxTurb = 1000;

var minpH = 0;
var maxpH = 14;

function setup(ranges)
{
    minTemp = ranges.minTemp;
    maxTemp = ranges.maxTemp;
}

function initSliders()
{ 
  var tempDiff = maxTemp - minTemp;

 $("#tempSlider").rangeSlider({
  bounds: {min: minTemp, max:maxTemp},
  defaultValues: {min:(tempDiff*0.25)+minTemp,max:(tempDiff*0.75)+minTemp},
  formatter:function(val){
         var value = Math.round(val);          
         return value.toString()  + "°C";     
      }});

 $("#pHSlider").rangeSlider({
  bounds: {min: minpH, max:maxpH},
  defaultValues: {min:minpH,max:maxpH},
  formatter:function(val){
         var value = Math.round(val);          
         return value.toString();     
      }});

 $("#saltSlider").rangeSlider({
   bounds: {min: minCond, max:maxCond},
defaultValues: {min:minCond,max:maxCond},
  formatter:function(val){
         var value = Math.round(val);          
         return value.toString()  + "";     
      }});

 $("#claritySlider").rangeSlider({
  bounds: {min: minTurb, max:maxTurb},
  defaultValues: {min:minTurb,max:maxTurb},
  formatter:function(val){
         var value = Math.round(val);          
         return value.toString()  + "";     
      }});
}


//Setting the preset temperature ranges
function presetTemp(id,low,high)
{
  $(id).click(function()
   {
    $("#tempSlider").rangeSlider("values", low, high);  
   });  
}

//Setting up preset temperature ranges
$(function()
{

presetTemp("#safe",minTemp,35);
presetTemp("#unsafe",36,maxTemp);
presetTemp("#hottest",Math.ceil(maxTemp*0.90),maxTemp);

});

$(function()
{
    $("#minTemp").val(Math.round($("#tempSlider").rangeSlider("values").min));
    $("#maxTemp").val(Math.round($("#tempSlider").rangeSlider("values").max));
  $("#tempSlider").bind("valuesChanged", function(e, data)
  {  
    $("#minTemp").val(Math.round(data.values.min));
    $("#maxTemp").val(Math.round(data.values.max));
  });
});

//Start Map
$(function()
{
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

