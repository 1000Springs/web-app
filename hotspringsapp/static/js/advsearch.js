function addCondition()
{
	var attribute;
	var condition;
   var logical;

	var selectedAtt = $("input[name=att]:checked");

	if (selectedAtt.length > 0)
	{
   	attribute = selectedAtt.val();
   }
   else
   {
      $("#alert #alertMessage").html("<strong>Warning!</strong> Attribute must be selected");
      $("#alert").show("fast");
      return;
   }

   var selectedCond = $("input[name=cond]:checked");

   if (selectedCond.length > 0)
	{
   	condition = selectedCond.val();
   }
   else
   {
      $("#alert #alertMessage").html("<strong>Warning!</strong> Condition must be selected");
      $("#alert").show("fast");
      return;
   }

   var constraint = $("input[name=const]").val();

   if(constraint == "")
   {
      $("#alert #alertMessage").html("<strong>Warning!</strong> Please input valid a constraint value");
      $("#alert").show("fast");
      return;   
   }


    var selectedLogical = $("input[name=logic]:checked");

   if (selectedLogical.length > 0)
   {
      logical = selectedLogical.val();
   }
   else
   {
      logical = "";
   }

   $("#conditions").append("<div><p>" +
      						   attribute + " " + condition + " " + constraint + " " + logical +
      						   '<button type="button" class="close" onclick="deleteSelected.call(this)">×</button> </p> <input type="hidden" name="conditions" value="'+ 
      						   attribute + "," + condition + "," + constraint +
      						   '"> </div>');
   $("#alert").hide();

}

function deleteSelected()
{
	$(this).closest("div").remove();
}

