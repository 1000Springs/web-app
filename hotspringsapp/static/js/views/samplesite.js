$(document).ready(function() {
	
	$.get('/chemistryJson/'+$('#sampleNumber').text())  
	  .done(function(data){
		  drawChemistryBubbleChart(data);
		  $('#chemistryViewLoading').hide();
		  $('#chemistryViewWrapper').show();
	  })
	  .fail(function(jqXHR, textStatus, errorThrown) {
		  $('#chemistryTab').html('<h3 style="height: 250px;">The chemistry data is coming soon</h3>');
	  });	
	
	$.get('/taxonomyJson/'+$('#sampleNumber').text())  
	  .done(function(data){
		  drawTaxonomyCollapsibleTree(data);
		  drawTaxonomicSunburst(data);
		  initTaxonomyViewToggle();
		  $('#diversityViewLoading').hide();
		  $('#diversityViewWrapper').show();
	  })
	  .fail(function(jqXHR, textStatus, errorThrown) {
		  $('#diversityTab').html('<h3 style="height: 250px;">The taxonomy data is coming soon</h3>');
	  });	
});

function initTaxonomyViewToggle() {
	$('.diversityToggleView').click(function(){
		$('.diversityView').toggle();
	});
	
	$('.diversityToggleHelp').click(function() {
		var toggleHelp = this;
		var helpText = $(this).closest('.diversityView').find('.diversityHelpText').first();
		if ($(helpText).is(":visible")) {
			$(helpText).slideUp(function(){
				$(toggleHelp).text('Show instructions');
			});
		} else {
			$(helpText).slideDown(function(){
				$(toggleHelp).text('Hide instructions');
			});			
		}	
	});		
}

function drawChemistryBubbleChart(bubbleData) {
	
	var w = 650 ,
	    h = 600,
	    r = 520,
	    x = d3.scale.linear().range([0, r]),
	    y = d3.scale.linear().range([0, r]),
	    node,
	    root;
	
	var pack = d3.layout.pack()
	    .size([r, r])
	    .value(function(d) { return d.size; })
	
	var vis = d3.select("#bubbles").insert("svg:svg", "h2")
	    .attr("width", w)
	    .attr("height", h)
	  .append("svg:g")
	    .attr("transform", "translate(" + (w - r) / 2 + "," + (h - r) / 2 + ")");
	
	
	    
	  node = root = bubbleData;
	
	  var nodes = pack.nodes(root);
	
	  vis.selectAll("#circle")
	      .data(nodes)
	      .enter()
	       .append("svg:circle")
	      .attr("class", function(d) { return d.children ? "bubbleVis parent" : "bubble bubbleVis"; })
	      .attr("title", function (d) {var d = this.__data__; return !(d.children) ? (d.name + ": " + d.value +  "ppm"):null })  
	      .attr("id", function(d){return d.name})  
	      .attr("cx", function(d) { return d.x; })
	      .attr("cy", function(d) { return d.y; })
	      .attr("r", function(d) { return d.r; })
	      .on("click", function(d) { return zoom(node == d ? root : d); });
	      
	  vis.selectAll("text")
	      .data(nodes)
	    .enter().append("svg:text")
	      .attr("class", function(d) { return d.children ? "parent" : "child"; })
	      .attr("x", function(d) { return d.x; })
	      .attr("y", function(d) { return d.y; })
	      .attr("dy", ".35em")
	      .attr("text-anchor", "middle")
	      .style("opacity", function(d) { return d.r > 20 ? 1 : 0; })
	      .text(function(d) { return d.name; });
	
	  d3.select(window).on("click", function() { zoom(root); });
	
	
	function zoom(d, i) {
	  var k = r / d.r / 2;
	  x.domain([d.x - d.r, d.x + d.r]);
	  y.domain([d.y - d.r, d.y + d.r]);
	
	  var t = vis.transition()
	      .duration(d3.event.altKey ? 7500 : 750);
	
	  t.selectAll("circle")
	      .attr("cx", function(d) { return x(d.x); })
	      .attr("cy", function(d) { return y(d.y); })
	      .attr("r", function(d) { return k * d.r; });
	
	  t.selectAll("text")
	      .attr("x", function(d) { return x(d.x); })
	      .attr("y", function(d) { return y(d.y); })
	      .style("opacity", function(d) { return k * d.r > 20 ? 1 : 0; });
	
	  node = d;
	  d3.event.stopPropagation();
	}		
}

function drawTaxonomyCollapsibleTree(treeData) {

	var w = 680,
	    h = 680,
	    node,
	    link,
	    root;
	
	var force = d3.layout.force()
	    .on("tick", tick)
	    .charge(function(d) {return d.depth * -10})
	    .gravity(0.1)
	    .linkDistance(25)
	    .size([w, h]);
	
	var vis = d3.select("#collapsibleTreeChart").insert("svg")
	    .attr("width", w)
	    .attr("height", h);
	
	root = treeData;
	root.fixed = true;
	root.x = w / 2;
	root.y = h / 2;
	window.maxCollapsibleTreeDepth = 8;
	
	update(true, window.maxCollapsibleTreeDepth);
	
	$('#collapsibleTreeTaxonomy .taxaSwatch').click(function(){
		var row =  $(this).closest('tr').index();
		window.maxCollapsibleTreeDepth = row + 1;
		update(false, window.maxCollapsibleTreeDepth);
	});
	
	function update(positionNodes, maxDepth) {
		
		var nodes = flatten(root, maxDepth);
		var links = d3.layout.tree().links(nodes);
		
		if (positionNodes) {
			nodes.forEach(function(d, i) {
			  d.x = w/2 + i;
			  d.y = h/2 + 100 * d.depth;
			});	
		}
	
		// Restart the force layout.
		force
		    .nodes(nodes)
		    .links(links)
		    .start();
	
		// Update the links…
		link = vis.selectAll("line.link")
		      .data(links, function(d) { return d.target.id; });
		
		// Enter any new links.
		link.enter().insert("svg:line", ".node")
		    .attr("class", function(d) { return (d.source.depth == 1) ? "root link" : "link";})
		    .attr("x1", function(d) { return d.source.x; })
		    .attr("y1", function(d) { return d.source.y; })
		    .attr("x2", function(d) { return d.target.x; })
		    .attr("y2", function(d) { return d.target.y; });
		
		// Exit any old links.
		link.exit().remove();
		
		// Update the nodes…
		node = vis.selectAll("circle.node")
		    .data(nodes, function(d) { return d.id; })
		    .style("fill", function (d) {
		    	var colour = getNodeColour(d);
		    	return colour;
		     });
		
		
		node.transition()
		    .attr("r", function(d) { return getNodeSize(d); });
		
		// Enter any new nodes.
		node.enter().append("svg:circle")
		 	.attr("class", function(d) { return (d.depth == 1) ? "root node" : "node";})
		    .attr("cx", function(d) { return d.x; })
		    .attr("cy", function(d) { return d.y; })
		    .attr("r", function(d) { return getNodeSize(d); })
		    .style("fill", function (d) { return getNodeColour(d); })
		    .on("click", click)
		    .call(force.drag);
		
		// Exit any old nodes.
		node.exit().remove();
	}
	
	function tick() {
	    // Calculate max/min node locations to keep within chart boundaries
        node.attr("cx", function(d) { 
    	        var r = getNodeSize(d);
    	  		return d.x = Math.max(r, Math.min(w - r, d.x)); })
	        .attr("cy", function(d) { 
	    	  	var r = getNodeSize(d); 
	    	  	return d.y = Math.max(r, Math.min(h - r, d.y)); });
      
	    link.attr("x1", function(d) { return d.source.x; })
	        .attr("y1", function(d) { return d.source.y; })
	        .attr("x2", function(d) { return d.target.x; })
	        .attr("y2", function(d) { return d.target.y; });
	

	}
	
	function getNodeSize(d) {
		return d.children ? 6 : Math.min(6 + (d.size / 200), 30);
	}
	
	function getNodeColour(d) {
		
		var colour;
		if (typeof d.taxa !== 'undefined') {
			if (d.selectedBranch) {
				colour = $('.' + d.taxa + 'Colour').css('color');
			} else {
				colour = $('.' + d.taxa + 'BackColour').css('background-color');
			}
		} else {
			colour = "#000000"
		}
		
		return colour;
	}
	
	// Toggle children on click.
	function click(d) {
		if (d.name != 'root') {
			clearSelectedTaxonomy();
			setSelectedTaxonomy(d);
			populateDetailBox(d.name);
			
			if (d.children) {
			  d._children = d.children;
			  d.children = null;
			} else {
			  d.children = d._children;
			  d._children = null;
			}
			update(false);
		}
	}
	
	function clearSelectedTaxonomy() {
		$("#collapsibleTreeTaxonomy .taxon").text("").attr("title", "");
		d3.selectAll('.selectedBranch').classed('selectedBranch', false);
		d3.selectAll('.node').each(function(node) { node.selectedBranch=false;});
	}
	
	function setSelectedTaxonomy(node) {
		
		if (node.name != "root") {
			$("#collapsibleTreeTaxonomy ." + node.taxa + "Name").text(node.name).attr("title", node.name);
			node.selectedBranch = true;
			setSelectedTaxonomy(getParentNode(node, true));
		}
	}
	
	function getParentNode(childNode, highlightLink) {
		var linkToParent = d3.selectAll('.link').filter(function(node){
			return node.target.id == childNode.id;
		});
		
		if (highlightLink && linkToParent.attr("class").indexOf("root") < 0) {
			linkToParent.attr("class", "link selectedBranch");
		}
		
		var parentNode = linkToParent[0][0].__data__.source;
		return parentNode;
	}
	
	function populateDetailBox(taxon) {
		if (window.lastCollapsibleTreeAjaxRequest) {
			window.lastCollapsibleTreeAjaxRequest.abort();
		}
		if ($('#collapsibleTreeTaxonDetailsName').text() != taxon) {
			$('#collapsibleTreeTaxonDetailsName').text(taxon);
			var firstSlash = taxon.indexOf('/');
			if (firstSlash >= 0) {
				taxon = taxon.substring(0, firstSlash);
			}
			
			$('#collapsibleTreeDetailWrapper').slideDown();
			
			$('#collapsibleTreeDetail').slideUp(function(){
				$('#collapsibleTreeAjaxWaiting').fadeIn(function(){
					window.lastCollapsibleTreeAjaxRequest = $.get('/taxon/'+taxon)  
					  .done(function(data){
						$('#collapsibleTreeAjaxWaiting').fadeOut(function(){
							$('#collapsibleTreeDetail').html(data);	
							$('#collapsibleTreeDetail').slideDown();
						});
					  })
					  .fail(function(jqXHR, textStatus, errorThrown) {
						$('#collapsibleTreeAjaxWaiting').fadeOut(function(){	
							if (errorThrown != "abort") {
								$('#collapsibleTreeDetail').html('<h4 class="taxonDetailsError">Unable to load summary</h4>');
								$('#collapsibleTreeDetail').slideDown();
							}
	
						});
					  })
					  .always(function(){
						  window.lastCollapsibleTreeAjaxRequest = null;
					  });
				});		
			});
		}
	}
	
	
	/*
	 * Returns a list of all nodes under the root, excluding nodes
	 * that have been collapsed by the user or are outside the
	 * maximum depth (taxonomy level) selected by the user.
	 */
	function flatten(root, maxDepth) {
		var nodes = [], i = 0;
		
		function recurse(node, depth) {
			var children = [];
			if (node.children) {
				children = node.children;
			} else if (node._children) {
				children = node._children;
			}
			
			if (node._children && typeof maxDepth !== 'undefined') {
				node.children = node._children;
				node._children = null;
			}
			if (node.children) {
				node.size = node.children.reduce(function(p, v) { return p + recurse(v, depth + 1); }, 0);
			} 
			if (!node.id) node.id = ++i;
			node.depth = depth;
			if (typeof maxDepth !== 'undefined' && depth >= maxDepth) {
				node._children = node.children;
				node.children = null;	
			} 
	
			if (typeof maxDepth === 'undefined' || depth <= maxDepth) {
				nodes.push(node);		
			}
		
			return node.size;
		}
		
		root.size = recurse(root, 1);
		return nodes;
	}	
	
} 

/**
 * This function is licensed under the Apache Licence, Version 2.0.
 * See http://www.apache.org/licenses/LICENSE-2.0.
 */
function drawTaxonomicSunburst(treeData) {
    var width = 680;
    var height = 680;
    var radius = Math.min(width, height) / 2;

    // Breadcrumb dimensions: width, height, spacing
    var b = {
      w: 270, h: 30, s: 3
    };

    // Total size of all segments; we set this later, after loading the data.
    var totalSize = 0; 

    var vis = d3.select("#sunburstChart").append("svg:svg")
        .attr("width", width)
        .attr("height", height)
        .append("svg:g")
        .attr("id", "sunburstContainer")
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    var partition = d3.layout.partition()
        .size([2 * Math.PI, radius * radius])
        .value(function(d) { return d.size; });

    var arc = d3.svg.arc()
        .startAngle(function(d) { return d.x; })
        .endAngle(function(d) { return d.x + d.dx; })
        .innerRadius(function(d) { return Math.sqrt(d.y); })
        .outerRadius(function(d) { return Math.sqrt(d.y + d.dy); });

    createVisualization(treeData);

    // Main function to draw and set up the visualization, once we have the data.
    function createVisualization(json) {

        // Basic setup of page elements.
        initializeBreadcrumbTrail();

        // Bounding circle underneath the sunburst, to make it easier to detect
        // when the mouse leaves the parent g.
        vis.append("svg:circle")
          .attr("r", radius)
          .style("opacity", 0);

        // For efficiency, filter nodes to keep only those large enough to see.
        var nodes = partition.nodes(json)
          .filter(function(d) {
          return (d.dx > 0.005); // 0.005 radians = 0.29 degrees
          });

        var colours = d3.scale.category20();

        var path = vis.data([json]).selectAll("path")
          .data(nodes)
          .enter().append("svg:path")
          .attr("display", function(d) { return d.depth ? null : "none"; })
          .attr("d", arc)
          .attr("fill-rule", "evenodd")
          .style("fill", function(d, i) { return colours(i); })
          .style("opacity", 1)
          .on("mouseover", mouseover);

        // Add the mouseleave handler to the bounding circle.
        d3.select("#sunburstContainer").on("mouseleave", mouseleave);

        // Get total size of the tree = value of root node from partition.
        totalSize = path.node().__data__.value;
    }

    // Fade all but the current sequence, and show it in the breadcrumb trail.
    function mouseover(d) {

        var percentage = (100 * d.value / totalSize).toPrecision(3);
        var percentageString = percentage + "%";
        if (percentage < 0.1) {
            percentageString = "< 0.1%";
        }

        d3.select("#sunburstPercentage").text(percentageString);
        d3.select("#sunburstTaxa").text(d.taxa).style('color', $('.' + d.taxa + 'Colour').css('color'));
        d3.select("#sunburstName").text(d.name);
        d3.select("#sunburstExplanation").style("visibility", "");

        var sequenceArray = getAncestors(d);
        updateBreadcrumbs(sequenceArray, percentageString);

        // Fade all the segments.
        d3.selectAll("path").style("opacity", 0.3);

        // Then highlight only those that are an ancestor of the current segment.
        vis.selectAll("path")
          .filter(function(node) { return (sequenceArray.indexOf(node) >= 0); })
          .style("opacity", 1);
    }

    // Restore everything to full opacity when moving off the visualization.
    function mouseleave(d) {

        // Hide the breadcrumb trail
        d3.select("#sunburstTrail")
          .style("visibility", "hidden");

        // Deactivate all segments during transition.
        d3.selectAll("path").on("mouseover", null);

        // Transition each segment to full opacity and then reactivate it.
        d3.selectAll("path")
          .transition()
          .duration(1000)
          .style("opacity", 1)
          .each("end", function() { d3.select(this).on("mouseover", mouseover); });

        d3.select("#sunburstExplanation")
          .transition()
          .duration(1000)
          .style("visibility", "hidden");
    }

    // Given a node in a partition layout, return an array of all of its ancestor
    // nodes, highest first, but excluding the root.
    function getAncestors(node) {
        var path = [];
        var current = node;
        while (current.parent) {
            path.unshift(current);
            current = current.parent;
        }
        return path;
    }

    function initializeBreadcrumbTrail() {
        // Add the svg area.
        var trail = d3.select("#sunburstSequence").append("svg:svg")
          .attr("width", 270)
          .attr("height", 300)
          .attr("id", "sunburstTrail");
    }

    // Generate a string that describes the points of a breadcrumb polygon.
    function breadcrumbPoints(d, i) {
        var points = [];
        points.push("0,0");
        points.push(b.w + ",0");
        points.push(b.w + "," + b.h);
        points.push("0," + b.h);

        return points.join(" ");
    }

    // Update the breadcrumb trail to show the current sequence and percentage.
    function updateBreadcrumbs(nodeArray, percentageString) {

        // Data join; key function combines name and depth (= position in sequence).
        var g = d3.select("#sunburstTrail")
          .selectAll("g")
          .data(nodeArray, function(d) { return d.name + d.depth; });

        // Add breadcrumb and label for entering nodes.
        var entering = g.enter().append("svg:g");

        entering.append("svg:polygon")
          .attr("points", breadcrumbPoints)
          .style("fill", function(d) { 
	          // gets the colour from the collapsibleTree table
	          return  $('.' + d.taxa + 'Colour').css('color');
           });

        entering.append("svg:text")
          .attr("x", 10)
          .attr("y", b.h / 2)
          .attr("dy", "0.35em")
          .attr("text-anchor", "left")
          .text(function(d) { return capitaliseFirstLetter(d.taxa) + ":"; });
        
        entering.append("svg:text")
         .attr("x", 70)
         .attr("y", b.h / 2)
         .attr("dy", "0.35em")
         .attr("text-anchor", "left")
         .text(function(d) { return d.name; });

        // Set position for entering and updating nodes.
        g.attr("transform", function(d, i) {
        	return "translate(0, " + i * (b.h + b.s) + ")";
        });

        // Remove exiting nodes.
        g.exit().remove();

        // Make the breadcrumb trail visible, if it's hidden.
        d3.select("#sunburstTrail")
          .style("visibility", "");

    }
}

function capitaliseFirstLetter(string)
{
    return string.charAt(0).toUpperCase() + string.slice(1);
}  


function addProgressBar(barAttr)
{	
	
	var barLength = barAttr.length;
	var barHeight = 30;
	
	var strokeWidth = 5;
	
	var x = barAttr.x+10;
	var y = barAttr.y+40;
	
	var progressX = x+(strokeWidth/2);	
	
	var max = barAttr.max;
	var current = barAttr.current;		

	var percentage = Math.ceil(current/max * (barLength-strokeWidth));
	
	var paper= barAttr.svg;	

	var units = barAttr.units;
	
	var pointerWidth = 10;
	var pointerHeight = 10;
	var progressArrow = paper.polygon([(progressX) - pointerWidth, y - pointerHeight,(progressX) + pointerWidth, y - pointerHeight],
									  [(progressX) + pointerWidth, y - pointerHeight,(progressX), y - 2.5],
									  [(progressX), y - 2.5, (progressX) - pointerWidth, y - pointerHeight]);
	
		progressArrow.animate({transform:"t"+percentage.toString()+",0s"},1000);
	
	progressArrow.attr({
	stroke: "#125e68",
	fill: "#125e68",
		strokeWidth: 0.5});
		
	//BAR
	
	
		var progress = paper.rect(progressX, y, 0, barHeight);
	progress.attr({
		fill: "#1D9BAB",
		stroke: "transparent",
		strokeWidth: strokeWidth		
	});

	progress.animate({width:percentage}, 1000);

	var outline = paper.rect(x, y, barLength, barHeight, 5);
	outline.attr({
		fill: "transparent",
		stroke: "#000",
		strokeWidth: strokeWidth
	});	
	
	
	var progressAmount = paper.text(0, y+10,0);
	progressAmount.attr({"class":"progressAmount"})
		
	if(current >= barAttr.warning)
	{
		progressAmount.attr({fill:"red"});
	}
		
	Snap.animate(0, current, function (value) {
		progressAmount.attr({text: Math.round(value*100)/100 + units});
	}, 1000);
			
	for(var i = 0;i < barAttr.markers.length;i++)
	{
		var marker = barAttr.markers[i]
		drawMarker(marker.name,marker.value,marker.height);		
	}
	
	for(var i = 0;i < barAttr.categories.length;i++)
	{			
		var cat = barAttr.categories[i];			
		drawCategoryRange(cat.name,cat.min,cat.max);
	}			

	for(var i = 0; i <=max; i+=(max/4))
	{	
	drawStep(i);
	
	
	}
			
	
	
	
	
	function drawMarker(text,value,height)
	{
		var markerLength = -10;			
		
			
		if(height != null)
		{
			markerLength *= height;			
		}
		
		
		
		var position = Math.ceil(value/max * (barLength-strokeWidth));
		var line = paper.line(progressX + position , y, progressX+position, y + markerLength);				
		line.attr({stroke: "Black",
				   strokeWidth: 1});
		
		var textLabel = paper.text(progressX+position, y - 20,text.toString());
		
		
		var textLabelWidth = textLabel.getBBox().width;
		var textLabelHeight = textLabel.getBBox().height;
	
		textLabel.remove();
		
		var textClearance = -5;

		textLabel = paper.text((progressX+position)-textLabelWidth/2+strokeWidth, (y + (textClearance)) + markerLength,text.toString());
		textLabel.attr({"class":"marker"});
	
	}

	function drawStep(value)
	{
		var markerLength = 10;

		var position = Math.ceil(value/max * (barLength-strokeWidth));
		var line = paper.line(progressX + position , y+(barHeight+markerLength), progressX+position, y+barHeight);				
		line.attr({stroke: "black",
				   strokeWidth: 1});

		if(value == 0 || value == max/2 || value == max)
		{
		var textLabel = paper.text(progressX+position, y+(barHeight+markerLength),value.toString() + units);

		var textLabelWidth = textLabel.getBBox().width;
		var textLabelHeight = textLabel.getBBox().height;
	

		textLabel.remove();

		var textClearance = 10;

		textLabel = paper.text((progressX+position)-(textLabelWidth/2), y+(barHeight+markerLength+textClearance),value.toString() + units);
		textLabel.attr({"class":"marker"});
		}

	}

	function drawCategoryRange(title,minRange,maxRange)
	{			
		var minPosition = Math.ceil((minRange/max) * (barLength-strokeWidth));
		var maxPosition = Math.ceil((maxRange/max) * (barLength-strokeWidth));
		
		
	
		
		
		var textLabel = paper.text(minPosition + progressX, y - 20,title.toString());
		textLabel.attr({"class":"marker"});
		
		var textLabelWidth = textLabel.getBBox().width;
		var textLabelHeight = textLabel.getBBox().height;
		textLabel.remove();
		
		markerTotalHeight =  y + barHeight + textLabelHeight;
		
		textLabel = paper.text(progressX + (maxPosition-minPosition)/2 - (textLabelWidth/2) + minPosition, markerTotalHeight + 30 + (barHeight+5)/2,title.toString());
		
		textLabel.attr({"class":"marker"});
		
			
		var categoryBox = paper.rect(minPosition + progressX, markerTotalHeight+30, maxPosition-minPosition, barHeight);
		categoryBox.attr({
			fill: "white",
			stroke: "Black",
			strokeWidth: strokeWidth		
		});
		
		
	}		
}