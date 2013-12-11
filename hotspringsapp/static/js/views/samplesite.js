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
	
	//Just finds the length of the string so that it can be positioned in the middle of the progressLine
	var progressAmount = paper.text(progressX, y - 20,current.toString());
	var progressAmountLength = progressAmount.getBBox().width;
	progressAmount.remove();
	
	progressAmount = paper.text(progressX+(barLength/2), y+20,0);
		
	if(current >= barAttr.warning)
	{
		progressAmount.attr({fill:"red"});
	}
		
	Snap.animate(0, current, function (value) {
		progressAmount.attr({text: Math.round(value)});
	}, 1000);
			
	for(var i = 0;i < barAttr.markers.length;i++)
	{
		var marker = barAttr.markers[i]
		drawMarker(marker.name,marker.value,marker.high);		
	}
	
	for(var i = 0;i < barAttr.categories.length;i++)
	{			
		var cat = barAttr.categories[i];			
		drawCategoryRange(cat.name,cat.min,cat.max);
	}			

	for(var i = 0; i < max/barAttr.step; i+=1)
	{	
	drawStep(i*barAttr.step);
	
	}
			
	var labelHigh = true;	
	var markerTotalHeight = 0;
	var alternatingBarHeight = barHeight;
	var labelTop = 1;
	
	function drawMarker(text,value,high)
	{
		var markerLength = 10;			
		var offset = 0;
		labelTop *= -1;
		if (labelHigh)
		{
			markerLength *= -1;
			offset = 0;
			labelHigh = false;
			alternatingBarHeight = 0 ;			
		}
		else
		{
			alternatingBarHeight = barHeight;
			labelHigh = true;
		}
		
		if(high)
		{
			
			markerLength *= 2;
			if(labelTop)
			{
				markerLength *= -2;
			}
		}
		
		
		
		var position = Math.ceil(value/max * (barLength-strokeWidth));
		var line = paper.line(progressX + position , y+alternatingBarHeight, progressX+position, y + alternatingBarHeight + markerLength);				
		line.attr({stroke: "Black",
				   strokeWidth: 1});
		
		var textLabel = paper.text(progressX+position, y - 20,text.toString());
		textLabel.attr
		({class:"label",
		fill:"white"});
		
		var textLabelWidth = textLabel.getBBox().width;
		var textLabelHeight = textLabel.getBBox().height;
		if( !labelHigh)
		{
			textLabelHeight = -5;
		}
		textLabel.remove();
		
		

		textLabel = paper.text((progressX+position)-textLabelWidth/2+strokeWidth, (y + alternatingBarHeight + (textLabelHeight)) + markerLength + offset,text.toString());
		textLabel.attr({class:"marker"});
	
	}

	function drawStep(value)
	{
		
		var position = Math.ceil(value/max * (barLength-strokeWidth));
		var line = paper.line(progressX + position , y, progressX+position, y+barHeight);				
		line.attr({stroke: "black",
				   strokeWidth: 1});

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