var max = 100;
var min = 0;


//Highlight filter items
$(function()
{
  $("#searchMenuItem").addClass("active");
  $(".filterIcons img").toggle(

  function()
  {
    $(this).animate(
    {
      "opacity": "1"
    }, "fast");
  }, function()
  {
    $(this).animate(
    {
      "opacity": "0.7"
    }, "fast");
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
   navigator.geolocation.getCurrentPosition(show_map);
   codeLatLng();
   $('img').tooltip();
 });

