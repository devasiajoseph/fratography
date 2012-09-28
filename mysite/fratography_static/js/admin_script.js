var Admin = {
    save_price_perhour:function(){
	
	var obj = {"value":["price"]};
	App.submit_data(obj,{},"/admin/save/price/perhour", Admin.seller_request_decision_callback, "loader");
    },
    save_price_perhour_callback:function(data){
	
    },
    add_availability:function(start, end, allDay){
	$("#id_available_start_date").val(start);
	$("#id_available_end_date").val(end);
	$("#id_available_id").val("");
	$('#modal-availability').modal({backdrop: false});
        $('#modal-availability').modal('show');
    },
    confirm_availability:function(){
	start_date = App.Util.format_date_str($("#id_available_start_date").val());
	end_date = App.Util.format_date_str($("#id_available_end_date").val());
	var submit_obj = {
	    "available_id":$("#id_available_id").val(),
	    "available_start_date":start_date,
	    "available_end_date":end_date};
	App.submit_data({}, submit_obj, "/admin/save/availability", Admin.confirm_availability_callback, "loader")
	
    },
    confirm_availability_callback:function(data){
	if ($("#id_available_id").val()){
	    event = $('#calendar').fullCalendar('clientEvents',$("#id_available_id").val())[0];
	    event.start = $("#id_available_start_date").val();
	    event.end = $("#id_available_end_date").val();
	    $('#calendar').fullCalendar('updateEvent', event);
	}else{
	    $('#calendar').fullCalendar('renderEvent',
					{id: data.id,
					 title: "Service Available",
					 start: $("#id_available_start_date").val(),
					 end: $("#id_available_end_date").val(),
					 allDay: false
					},
					true // make the event "stick"
				       );
	}
       $('#modal-availability').modal('hide');
    },
    edit_event:function(event) {
        $("#id_available_start_date").val(event.start);
	$("#id_available_end_date").val(event.end);
        $("#id_available_id").val(event.id);
	$('#modal-availability').modal({backdrop: false});
        $('#modal-availability').modal('show');
    },
    remove_availability:function(){
	
	$('#calendar').fullCalendar('removeEvents',[$("#id_available_id").val()]);
        $('#modal-availability').modal('hide');
    }
}