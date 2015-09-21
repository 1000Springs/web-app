
function log10(val)
{
  if(val === 0)
  {
    return 0;
  }
  return Math.log(val) / Math.LN10;
}

function loadData(endPoint, params, label, scaleLabel)
{
 $(".loading").show();
$.get(endPoint + params)
      .done(function(data){

      $(".loading").hide();
        makeChart(data, label, scaleLabel);
      })
      .fail(function(jqXHR, textStatus, errorThrown) {
         $('#dataTab').html('<h4 style="height: 250px;">An error occurred downloading data</h4>');
      });

}




$(document).ready(function() {


loadData('/overviewGraphJson/',"sulfate", "Sulfate", "ppm");
$('#chemList').val("sulfate").trigger("chosen:updated");

$('#chemList').on('change', function(evt, params) {
   d3.select("#newGraph").select("svg").remove();
   loadData("overviewGraphJson/", $(this).val(), $('#chemList option:selected').text(), "ppm");

  });

$('#taxLvlList').on('change', function(evt, params) {
        $.get('/overviewTaxonTypes/'+ $(this).val())
         .done(function(data){

          names = data["types"];
          var sel = $("#taxNameList")
          sel.empty();
          for(var i = 0; i < names.length; i++) {
              var opt = document.createElement('option');
              opt.innerHTML = names[i];
              opt.value = encodeURIComponent(names[i]);
              sel.append(opt);
          }
         })
         .fail(function(jqXHR, textStatus, errorThrown) {
            var sel = $("#taxNameList")
            sel.empty();

            var opt = document.createElement('option');
            opt.innerHTML = "Data not found"
            opt.value = "n/a"
            sel.append(opt);

         });
  });
$('#taxonSearch').on('click', function(evt, params) {

          d3.select("#newGraph").select("svg").remove();
          var domainPhylum = $("#taxNameList").val();
          loadData('/overviewTaxonGraphJson/'+$('#taxLvlList').val()+"/",domainPhylum, domainPhylum, "%");
  });




});

function makeChart(plots,colName, scaleLabel)
{

data = plots["plots"].slice();
var percentage = 0.95;
var margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;
var removeFromEachEnd = Math.ceil(data.length * (1-percentage))/2;
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
var max = d3.max(data, function(d) { return d.value;} );
var min = d3.min(data, function(d) { if(d.value>0) return d.value;});

var localMax = d3.max(data, function(d) { if(d.index<(data.length-removeFromEachEnd)) return d.value;});
var localMin = d3.min(data, function(d) { if(d.value>0 && d.index>removeFromEachEnd) return d.value;});

var counter = 0

var plotColours = function(d) {
    var normFirst = false;
    var value = d.value/localMax;
    var colour = 0;

    if(d.value === null || d.value <= 0) {
    	// values that were below the detection limit will appear as white dots,
    	// and won't be counted in the colour scale calculation
    	colour = null;
    	
    } else if(counter >= removeFromEachEnd || counter <=(data.length-removeFromEachEnd)) {
	    // Gets a percentage of the values starting at the median i.e 95% of the values would mean we'd exclude the first and last 2.5% of the data plots
	    //This will return a number between 1 and 254, as 0 and 255 are taken up by values outside of the percentage threshold
	    colour =  1+(253-(Math.floor((((d.value) - (localMin))/((localMax)-(localMin)))*253)));
	    
    } else if(counter <= removeFromEachEnd ) {
    	colour = 255;
    	
    } else if ( counter >=(data.length-removeFromEachEnd)) {
    	colour = 0;
    }
    
    if (colour === null) {
    	return "rgb(255,255,255)";
    } else {
    	counter++;
    	return "rgb(255,"+colour+",0)";
    }
};

var svg = d3.select("#newGraph").append("svg")
    .attr("width", width + margin.left + margin.right +64)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


  x.domain(d3.extent(data, function(d) { return d.pH; })).nice();
  y.domain(d3.extent(data, function(d) { return d.temperature; })).nice();

  tip = d3.tip().attr('class', 'd3-tip').html(function(d) {
    columnName = 0
    if(d.value!==null)
    {
      if(d.value < 0)
      {
    	// below detection limit
        columnName = '< '+Math.abs(d.value);
      }
      else
      {
      columnName = d.value;
      }
    }
    else
    {
      columnName = "N/A";
    }

    var tooltip = "pH: " + d.pH + " " + "Temp: " + d.temperature + " " + colName+": "+columnName;
    return tooltip;

  });
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
      .attr("class","graph-text")
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
      .attr("class","graph-text")
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
      .style("fill", function(d) { return plotColours(d) })
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
       window.location = "/samplesite/"+d.id;
    });


     var key = svg.append("g")
    .attr("class", "key")
    .attr("height", 0)
    .attr("width", 0)
    .attr('transform', 'translate(5,200)');

    var keyValue = key.append("text")
    .attr("x", width - 18)
    .attr("y", -5);

    var legend = svg.append("g")
    .attr("class", "legend")
    .attr("height", 0)
    .attr("width", 0)
    .attr('transform', 'translate(5,50)');

    legend.append("text")
    .attr("x", width - 25)
    .attr("y", -5)
    .text( min);

    legend.append("text")
    .attr("x", width - 25)
    .attr("y", 105)
    .text( max);
    
    legend.append("text")
    .attr("x", width)
    .attr("y", 50)
    .text(scaleLabel);    


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
