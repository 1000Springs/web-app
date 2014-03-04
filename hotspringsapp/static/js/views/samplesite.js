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
	progressAmount.attr({class:"progressAmount"})
		
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
		textLabel.attr({class:"marker"});
	
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
		textLabel.attr({class:"marker"});
		}

	}

	function drawCategoryRange(title,minRange,maxRange)
	{			
		var minPosition = Math.ceil((minRange/max) * (barLength-strokeWidth));
		var maxPosition = Math.ceil((maxRange/max) * (barLength-strokeWidth));
		
		
	
		
		
		var textLabel = paper.text(minPosition + progressX, y - 20,title.toString());
		textLabel.attr({class:"marker"});
		
		var textLabelWidth = textLabel.getBBox().width;
		var textLabelHeight = textLabel.getBBox().height;
		textLabel.remove();
		
		markerTotalHeight =  y + barHeight + textLabelHeight;
		
		textLabel = paper.text(progressX + (maxPosition-minPosition)/2 - (textLabelWidth/2) + minPosition, markerTotalHeight + 30 + (barHeight+5)/2,title.toString());
		
		textLabel.attr({class:"marker"});
		
			
		var categoryBox = paper.rect(minPosition + progressX, markerTotalHeight+30, maxPosition-minPosition, barHeight);
		categoryBox.attr({
			fill: "white",
			stroke: "Black",
			strokeWidth: strokeWidth		
		});
		
		
	}		
}