var max = 150;
var min = 0;

//Slider code
$(function()
{
  $("#slider-range").slider(
  {
    range: true,
    min: min,
    max: max,
    animate: "fast",
    values: [25, 75],
    change: function(event, ui)
    {
      $("#amount").val($("#slider-range").slider("values", 0) + "°C" + " - " + $("#slider-range").slider("values", 1) + "°C");
    },
    slide: function(event, ui)
    {
      $("#amount").val(ui.values[0] + "°C - " + ui.values[1] + "°C");
    }
  });
  $("#amount").val($("#slider-range").slider("values", 0) + "°C" + " - " + $("#slider-range").slider("values", 1) + "°C");
});



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
    $( "#slider-range" ).slider( "values", 1, high );
    setTimeout(function() {$( "#slider-range" ).slider( "values", 0, low )},150);      
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

