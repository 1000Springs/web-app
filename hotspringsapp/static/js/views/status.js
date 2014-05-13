function statusGraph(element,pos)
			{
				/* Pointer Parameters */
				var position = pos;
				var pointerWidth = 7.5;
				var pointerHeight = 10;
			
				/* Circle Parameters */
				var strokeWidth = 2;
				var distanceApart = 150;
				var radius = 15;			
				var startX = (radius/2)-5;
				var startY = (radius*2) + pointerHeight;
				var numberOfSteps = 3;
				
				/* Text Parameters */				
				var distanceAboveCircle = 10;
				var stepHeadings = ["Physical Measurements","Chemistry","Sequencing Data","Complete"];
				
				var s = Snap(element);
							
				
				for(var i = 0; i <= numberOfSteps; i++)
				{
					
					
					var stage1Heading = s.text(startX, startY-(radius+distanceAboveCircle),stepHeadings[i]);
					var width = stage1Heading.getBBox().width;
					stage1Heading.remove();	
					if(i == 0)
					{	
						/* moves the svg by half the width of the word so that it fits on the page*/
						startX+=(width/2);
					}					
					var stage1Heading = s.text(startX-(width/2) + (i*(distanceApart+strokeWidth)) , startY-(radius+distanceAboveCircle),stepHeadings[i]);
					
					var stage1 = s.circle(startX + (i*(distanceApart+strokeWidth)), startY, radius);
					var colour = "#1D9BAB";
					if(i > position)
					colour = "#FFF";
					
					
					
					stage1.attr({
						fill: colour,
						stroke: "#000",
						strokeWidth: strokeWidth
					});
					
					if(i == numberOfSteps)
					{
						break;
					}
					var stage1_2 = s.line(startX+radius+(strokeWidth/2) + (i*(distanceApart+strokeWidth)),startY,startX+(strokeWidth/2)+ distanceApart-radius + (i*(distanceApart+strokeWidth)),startY);
					stage1_2.attr({					
						stroke: "#000",
						strokeWidth: 1
					});
					
				
					
				}
				
				/* position increased by one because the pointer should always be one ahead of the coloured circles */
				position++;
				if(position<numberOfSteps)
				{
				var pX = startX;
				var pY = startY + radius + strokeWidth + 5 ;
				var pointer = s.polygon([pX + (position * (distanceApart + strokeWidth)), pY, -pointerWidth+ pX + (position * (distanceApart + strokeWidth)), pointerHeight+ pY],[pX+ (position * (distanceApart + strokeWidth)), pointerHeight + pY, pointerWidth + pX + (position * (distanceApart + strokeWidth)), pointerHeight + pY]);
				
				pointer.attr({
				fill: "#1D9BAB",
				stroke: "#1D9BAB"
				
				});
				}	
				
			}
