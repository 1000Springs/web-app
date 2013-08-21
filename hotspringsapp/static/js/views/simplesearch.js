var max = 100;
var min = 0;

// Start slider
$(function()
{

 $("#slider").rangeSlider({
  formatter:function(val){
         var value = parseInt(Math.round(val * 5) / 5);
          
         return value.toString()  + "°C";
     
      }});
});


// $(function()
// {
//   // $("#searchMenuItem").addClass("active");
//   $(".filterIcons img").toggle(

//   function()
//   {
//     $(this).animate(
//     {
//       "opacity": "1"
//     }, "fast");
//   }, function()
//   {
//     $(this).animate(
//     {
//       "opacity": "0.7"
//     }, "fast");
//   });
// });


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
    $("#minTemp").val(Math.round(parseInt($("#slider").rangeSlider("values").min) * 5) / 5);
    $("#maxTemp").val(Math.round(parseInt($("#slider").rangeSlider("values").max) * 5) / 5);
  $("#slider").bind("valuesChanged", function(e, data)
  {  
    $("#minTemp").val(Math.round(parseInt(data.values.min) * 5) / 5);
    $("#maxTemp").val(Math.round(parseInt(data.values.max) * 5) / 5);
  });
});

//Start Map
$(function()
{
   navigator.geolocation.getCurrentPosition(show_map);
   codeLatLng();
   $('img').tooltip();
 });

