var Admin = {
    save_price_perhour:function(){
	
	var obj = {"value":["price"]};
	App.submit_data(obj,{},"/admin/save/price/perhour", Admin.seller_request_decision_callback, "loader");
    },
    save_price_perhour_callback:function(data){
	
    },
    add_availability:function(start, end, allDay){
	$("#id_start").val(start);
	$("#id_end").val(end);
	$("#id_id").val("");
	$('#modal-availability').modal({backdrop: false});
        $('#modal-availability').modal('show');
    },
    confirm_availability:function(){
	var obj = {"value":["start","end"]}
	App.submit_data(obj, {"event_type":"availability"}, "/admin/save/availability", Admin.confirm_availability_callback, "loader")
	
    },
    confirm_availability_callback:function(data){
	if ($("#id_id").val()){
	    event = $('#calendar').fullCalendar('clientEvents',$("#id_id").val())[0];
	    event.start = $("#id_start").val();
	    event.end = $("#id_end").val();
	    $('#calendar').fullCalendar('updateEvent', event);
	}else{
	    $('#calendar').fullCalendar('renderEvent',
					{id: data.id,
					 title: "Service Available",
					 start: $("#id_start").val(),
					 end: $("#id_end").val(),
					 allDay: false
					},
					true // make the event "stick"
				       );
	}
       $('#modal-availability').modal('hide');
    },
    edit_event:function(event) {
        $("#id_start").val(event.start);
	$("#id_end").val(event.end);
        $("#id_id").val(event.id);
	$('#modal-availability').modal({backdrop: false});
        $('#modal-availability').modal('show');
    },
    remove_availability:function(){
	console.log($("#id_id").val());
	submit_obj = {"id":$("#id_id").val()}
	App.submit_data({}, submit_obj,"/admin/remove/availability", function(data){
	    $('#calendar').fullCalendar('removeEvents',[$("#id_id").val()]);
            $('#modal-availability').modal('hide');
	}, "loader");
    },
    save_album:function(form){
	var obj = {"value":["id","name", "cover_photo"]};
	App.submit_data_iframe(form, obj, "loader");
    },
    save_album_callback:function(id){
	$("#id_id").val(id);
	$("#id_album_id").val(id);
	$("#album_delete_button").show();
	$("#images_container_widget").show();
    },
    delete_album:function(){
	var obj = {"value":["id"]};
	App.submit_data(obj, {}, "/admin/album/delete", Admin.delete_album_callback, "loader");
    },
    delete_album_callback:function(){
	window.location.href = "/admin/album/list/1";
    },
    add_category:function(parent){
	$("#id_parent").val(parent);
	$("#id_object_id").val("");
	$("#add-category").modal({show:true, backdrop:false});
    },
    add_subcategory:function(){
	console.log($("#id_category_parent").val());
	Admin.add_category($("#id_category_parent").val());
	
    },
    save_category:function(){
	var obj = {"value":["object_id", "parent", "name"]};
	App.submit_data(obj, {}, "/admin/album/category/save", Admin.save_category_callback, "loader");
    },
    save_category_callback:function(){
	window.location.reload();
    },
    edit_category:function(object_id){
	App.get_data("/admin/album/category/get", {"object_id":object_id},
		     function(data){
			 $("#id_object_id").val(data["object_id"]);
			 $("#id_parent").val(data["parent"]);
			 $("#id_name").val(data["name"]);
			 $("#add-category").modal({show:true, backdrop:false});
		     },
		     "loader");
    },
    delete_category:function(object_id){
	var submit_obj = {"object_id":object_id};
	App.submit_data({}, submit_obj, "/admin/album/category/delete", Admin.delete_category_callback, "loader");
    },
    delete_category_callback:function(data){
	$("#container_"+data["object_id"]).remove();
    },
    get_subcategories:function(object_id){
	$("#id_category_parent").val(object_id);
	App.get_data("/admin/album/category/sub", {"object_id":object_id},
		     function(data){
			 $("#subcategory_container").html("");
			 for (i in data["subcategories"]){
			     var subcategory_view = new SubCategoryView({ el: $("#subcategory_container"),
									  "subcategory":data["subcategories"][i] });
			 }
			 $("#subcategory_holder").show();
		     },
		     "loader");
    }
    
}

SubCategoryView = Backbone.View.extend({
        initialize: function(attrs){
	    this.options = attrs;
            this.render();
        },
        render: function(){
            // Compile the template using underscore
            var template = _.template( $("#subcategory_template").html(), this.options.subcategory );
            // Load the compiled HTML into the Backbone "el"
            this.$el.append( template );
        }
    });
