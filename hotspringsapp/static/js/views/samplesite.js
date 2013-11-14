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
	
	
	
	
	var progressLine = paper.line(progressX, y+2, progressX, y - 20);
	
	progressLine.attr({
	stroke: "black",
		strokeWidth: 1});
		
	//Just finds the length of the string so that it can be positioned in the middle of the progressLine
	var progressAmount = paper.text(progressX+percentage, y - 20,current.toString());
	var progressAmountLength = progressAmount.getBBox().width;
	progressAmount.remove();
	
	progressAmount = paper.text(progressX, y - 21,0);

	//BAR
	
	
		var progress = paper.rect(progressX, y, 0, barHeight);
	progress.attr({
		fill: "#1D9BAB",
		stroke: "transparent",
		strokeWidth: strokeWidth		
	});

	progress.animate({width:percentage}, 1000);
	progressLine.animate({x2:progressX+percentage}, 1000);
	progressLine.animate({x1:progressX+percentage}, 1000);
	progressAmount.animate({text:current.toString()},1000);
	progressAmount.animate({x:(progressX-progressAmountLength/2)+percentage},1000);

			var outline = paper.rect(x, y, barLength, barHeight, 5);
	outline.attr({
		fill: "transparent",
		stroke: "#000",
		strokeWidth: strokeWidth
	});		
	
	
			
	for(var i = 0;i < barAttr.markers.length;i++)
	{
		var marker = barAttr.markers[i]
		drawMarker(marker.name,marker.value);		
	}
	
	for(var i = 0;i < barAttr.categories.length;i++)
	{			
		var cat = barAttr.categories[i];			
		drawCategoryRange(cat.name,cat.min,cat.max);
	}	
			
			
	var labelHigh = true;	
	var markerTotalHeight = 0;
	function drawMarker(text,value)
	{
		var markerLength = 10;			
		var offset = 0;
		if (labelHigh)
		{
			markerLength *= 2
			offset = 0;
			labelHigh = false;
		}
		else
		{
			labelHigh = true;
		}
		
		var position = Math.ceil(value/max * (barLength-strokeWidth));
		var line = paper.line(progressX + position , y+barHeight, progressX+position, y + barHeight + markerLength);				
		line.attr({stroke: "Black",
				   strokeWidth: 1});
		
		var textLabel = paper.text(progressX+position, y - 20,text.toString());
		textLabel.attr({class:"label"});
		
		var textLabelWidth = textLabel.getBBox().width;
		var textLabelHeight = textLabel.getBBox().height;
		textLabel.remove();
		
		markerTotalHeight =  y + barHeight + textLabelHeight;

		textLabel = paper.text((progressX-textLabelWidth/2)+position, markerTotalHeight + markerLength + offset,text.toString());
		textLabel.attr({class:"label"});
	
	}

	function drawCategoryRange(title,minRange,maxRange)
	{			
		var minPosition = Math.ceil((minRange/max) * (barLength-strokeWidth));
		var maxPosition = Math.ceil((maxRange/max) * (barLength-strokeWidth));
		
		
		
		var categoryBox = paper.rect(minPosition + progressX, markerTotalHeight+30, maxPosition-minPosition, barHeight);
		categoryBox.attr({
			fill: "white",
			stroke: "Black",
			strokeWidth: strokeWidth		
		});
		
		
		
		var textLabel = paper.text(minPosition + progressX, y - 20,title.toString());
		textLabel.attr({class:"label"});
		
		var textLabelWidth = textLabel.getBBox().width;
		var textLabelHeight = textLabel.getBBox().height;
		textLabel.remove();
		

		
		textLabel = paper.text(progressX + (maxPosition-minPosition)/2 - (textLabelWidth/2) + minPosition, markerTotalHeight + 30 + (barHeight+5)/2,title.toString());
		
		textLabel.attr({class:"label"});
		
	}		
}