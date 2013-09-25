// Start slider
var minTemp = 0;
var maxTemp = 100;

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
  bounds: {min: 0, max:14},
  defaultValues: {min:4,max:10},
  formatter:function(val){
         var value = Math.round(val);          
         return value.toString();     
      }});

 $("#saltSlider").rangeSlider({
   bounds: {min: 0, max:100},
defaultValues: {min:30,max:70},
  formatter:function(val){
         var value = Math.round(val);          
         return value.toString()  + "";     
      }});

 $("#claritySlider").rangeSlider({
  bounds: {min: 0, max:100},
  defaultValues: {min:30,max:70},
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

function hideSlider(button,slider)
{  


  $(button).click(function()
  {
    if($(slider).is(":visible"))
    {
      $(button).html("show")
      $(slider).hide("fast");
    }
    else
    {
      $(button).html("hide")
      $(slider).show("fast");
    }
  });
}


//Setting up preset temperature ranges
$(function()
{

presetTemp("#safe",minTemp,35);
presetTemp("#unsafe",36,maxTemp);
presetTemp("#hottest",Math.ceil(maxTemp*0.90),maxTemp);

hideSlider("#phHide","#pHSlider");
hideSlider("#saltHide","#saltSlider");
hideSlider("#clarityHide","#claritySlider");

$("#phHide").trigger("click");
$("#saltHide").trigger("click");
$("#clarityHide").trigger("click");

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

