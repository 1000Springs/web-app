// Start slider
var minTemp = 0;
var maxTemp = 100;

var minCond = 0;
var maxCond = 2000000;

var minTurb = 0;
var maxTurb = 2500;

var minpH = -1;
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
  setMinMaxVals("#minTemp","#maxTemp","#tempSlider");
  setMinMaxVals("#minPH","#maxPH","#pHSlider");
  setMinMaxVals("#minTurb","#maxTurb","#claritySlider");
  setMinMaxVals("#minCond","#maxCond","#saltSlider");
});

function setMinMaxVals(minVal,maxVal,elementId)
{
   $(minVal).val(Math.round($(elementId).rangeSlider("values").min));
    $(maxVal).val(Math.round($(elementId).rangeSlider("values").max));
  $(elementId).bind("valuesChanged", function(e, data)
  {  
    $(minVal).val(Math.round(data.values.min));
    $(maxVal).val(Math.round(data.values.max));
  });
}

//Start Map
$(function()
{
   $('img').tooltip();
 });



