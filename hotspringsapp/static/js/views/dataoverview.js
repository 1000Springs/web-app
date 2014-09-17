
function log10(val)
{
  if(val === 0)
  {
    return 0;
  }
  return Math.log(val) / Math.LN10;
}

function loadData(columnName)
{
$.get('/overviewGraphJson/'+ columnName)  
      .done(function(data){
        console.log(data);
        makeChart(data,columnName);
      })
      .fail(function(jqXHR, textStatus, errorThrown) {
        // $('#chemistryTab').html('<h4 style="height: 250px;">The chemistry data for this site is coming soon</h4>');
        console.log("Not working");
      });

}




$(document).ready(function() {

loadData("sulfate");
$('#chemList').val("sulfate").trigger("chosen:updated");

$('#chemList').on('change', function(evt, params) {
   d3.select("#newGraph").select("svg").remove();
   loadData($(this).val());

  });


});

function makeChart(plots,colName)
{

var data = plots["plots"].slice();
var margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var cRadius = 5;
var cRadiusHover = 10;
var cBorder = 1;
var cBorderHover = 3;

var x = d3.scale.linear()
    .range([0, width]);

var y = d3.scale.linear()
    .range([height, 0]);

var color = d3.scale.category10();

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");
var max = d3.max(data, function(d) { return +d.sulfate;} );  
var min = d3.min(data, function(d) { if(d.sulfate<0)return 0; 
                                     else return  +d.sulfate;});
console.log(min);
console.log(max);

var plotColours = function(d){ 

  var normFirst = false;
  var sulfate = d.sulfate/max;

  var colour = 0;

  if(!normFirst)
  colour = 255-(Math.floor(((log10(d.sulfate) - log10(min))/(log10(max)-log10(min)))*255));
  else
  colour =  Math.floor(Math.abs(log10(sulfate) - log10(min))/(log10(max)-log10(min))*255);

  // console.log("sulfate " + d.sulfate);
  // console.log("log10 sulfate " + log10(d.sulfate));

  //   console.log("min: " + min);
  //   console.log("max: " + max); 
  //   console.log("log10 min: " + log10(min));
  //   console.log("log10 max: " + log10(max)); 
  //   console.log("Top: " + (log10(d.sulfate) - log10(min)));
  //   console.log("Bottom: " + (log10(max)-log10(min)));
  //   console.log(colour)

  return colour;
};

var svg = d3.select("#newGraph").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  

  data.forEach(function(d) {
    d.temperature = +d.temperature;
    d.pH = +d.pH;    
    // console.log("sulfate: " + log10(d.sulfate));
    // console.log("min: " + log10(min));
    // console.log("max: " + log10(max)); 

    // console.log("sulfate: " + d.sulfate);
    // console.log("min: " + min);
    // console.log("max: " + max);
  });


  x.domain(d3.extent(data, function(d) { return d.pH; })).nice();
  y.domain(d3.extent(data, function(d) { return d.temperature; })).nice();
  
  tip = d3.tip().attr('class', 'd3-tip').html(function(d) { return "pH:" + d.pH + " " + "Temp:" + d.temperature + " " + colName+":"+d.sulfate});
  svg.call(tip)
  tip.offset([-10, 0])
  

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
    .append("text")
      .attr("class", "label")
      .attr("x", width)
      .attr("y", -6)
      .style("text-anchor", "end")
      .text("pH");

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("class", "label")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Temperature")

  svg.selectAll(".dot")
      .data(data)
    .enter().append("circle")
      .attr("class", "dot")
      .attr("r", 5)
      .attr("cx", function(d) { return x(d.pH); })
      .attr("cy", function(d) { return y(d.temperature); })
    .attr("title", function(d) { return d.id})
    .attr("stroke","black")
      .style("fill", function(d) { return "rgb(255,"+plotColours(d)+",0)" }) 
    .on("mouseover", function(d) {
       d3.select(this).attr("r", 10)
       .attr("stroke-width",cBorderHover);
       tip.show(d);      
    })
    .on("mouseout",  function(d) {
      d3.select(this).attr("r", 5)
      .attr("stroke-width",cBorder);
      tip.hide(d);
    })
    .on("click", function(d){
       
    });
    
    var legend = svg.append("g")
    .attr("class", "legend")
    .attr("height", 0)
    .attr("width", 0)
    .attr('transform', 'translate(5,50)');

    legend.append("text")
    .attr("x", width - 18)
    .attr("y", -5)
    .text( 0);

    legend.append("text")
    .attr("x", width - 18)
    .attr("y", 105)
    .text( max);


    legend.append("rect")
      .attr("x", width - 18)
      .attr("width", 15)
      .attr("height", 90)
      .style("fill", "url(#gradient)")
      .style("stroke","black"); 

      var gradient = svg.append("svg:defs")
  .append("svg:linearGradient")
    .attr("id", "gradient")
    .attr("x1", "50%")
    .attr("y1", "0%")
    .attr("x2", "50%")
    .attr("y2", "100%")
    .attr("spreadMethod", "pad");
 
gradient.append("svg:stop")
    .attr("offset", "0%")
    .attr("stop-color", "rgb(255,255,0)")
    .attr("stop-opacity", 1);
 
gradient.append("svg:stop")
    .attr("offset", "100%")
    .attr("stop-color", "rgb(255,0,0)")
    .attr("stop-opacity", 1);  


}


