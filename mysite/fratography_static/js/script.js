var App = {
    submit_data : function(obj, submit_obj, url, callback, loader_id, no_message) {
	$("#message___all__").hide();
	if(no_message){
	    App.show_loader("None", loader_id);
	}else{
            App.show_loader("Submitting", loader_id);
	}
        for(var i in obj["value"]){
            $("#message_"+ obj["value"][i]).html("");
            $("#container_"+ obj["value"][i]).removeClass("error");
            submit_obj[obj["value"][i]] = $("#id_" + obj["value"][i]).val();
        }
        for(var j in obj["check"]){
            if($("#id_"+obj["check"][j]).is(':checked')){
                submit_obj[obj["check"][j]] = "True";//$("#id_"+obj["check"][j]).attr('value');
            }else{
                submit_obj[obj["check"][j]] = "False";//obj["check"][j]["unchecked_value"];
            }
        }
        for(var k in obj["check_group"]){
            var check_group = document.getElementsByName(obj["check_group"][k]);
            var added_counter = 0;
            for(cg_counter=0;cg_counter<check_group.length; cg_counter++){
                if($(check_group[cg_counter]).is(':checked')){
                    if(added_counter === 0){
                        submit_obj[obj["check_group"][k]+"_alias"] = $(check_group[cg_counter]).attr('value')+",";
                    }else{
                        submit_obj[obj["check_group"][k]+"_alias"] = submit_obj[obj["check_group"][k]+"_alias"]+$(check_group[cg_counter]).attr('value')+",";
                    }
                    added_counter++;
                }
            }
        }
        submit_obj["csrfmiddlewaretoken"] = $('input[name="csrfmiddlewaretoken"]')[0].value;
        $.post(url, submit_obj, function(data){
            App.hide_loader(loader_id);
            App.process_data(data, callback);
        }).error(function(xhr){
	    App.hide_loader(loader_id);
	    App.handle_ajax_error(xhr);
	});
    },
    handle_ajax_error:function(xhr){
	switch (xhr.status){
	    case 404:
	    App.show_error("Requested function not found");
	    break;
	    case 403:
	    App.show_error("You don't have access to perform this action");
	    break;
	    case 500:
	    App.show_error("A system error has occured.");
	    break;
	    default:
	    App.show_error("Error!!!");
	};

    },
    submit_data_iframe:function(form, obj, loader_id){
	$("#message___all__").hide();
	App.hide_error();
	App.hide_info();
	App.hide_warning();
        App.show_loader("Submitting", loader_id);
	for(var i in obj["value"]){
            $("#message_"+ obj["value"][i]).html("");
            $("#container_"+ obj["value"][i]).removeClass("error");
        }
        for(var j in obj["check"]){
            $("#message_"+ obj["value"][i]).html("");
            $("#container_"+ obj["value"][i]).removeClass("error");
        }
	$("#"+form).submit();
    },
    get_data:function(url, data, callback, loader_id){
	App.show_loader("None", loader_id);
	$.get(url, data, function(data){
	    App.hide_loader(loader_id);
            App.process_data(data, callback, true);
	});
    },
    get_raw_data:function(url, data, callback, loader_id){
	App.show_loader("None", loader_id);
	$.get(url, data, function(data){
	    App.hide_loader(loader_id);
	    callback(data);
	});
    },
    process_data : function(data_str, callback, is_json){
	
	if (is_json){
	    data = data_str;
	}else{
	    data = JSON.parse(data_str);
	}
	
        switch (data["code"]){
        case "form_error":
            App.process_error(data["errors"]);
            App.show_error(App.code_message[data["code"]]);
            break;
        case "system_error":
            App.show_error(App.code_message[data["code"]]);
            break;
        case "callback":
            callback(data);
            break;
        case "invalid_request":
            App.show_error(App.code_message[data["code"]]);
            callback(data);
            break;
        case "registered":
            window.location.href = data["success_page"];
            break;
        case "login":
            callback(data);
            break;
        case "data_loaded":
            callback(data);
            break;
	case "server_message":
            App.show_info(App.code_message[data["server_message"]]);
            break;
	case "saved":
            App.show_info(App.code_message[data["code"]]);
	    if (callback){
		callback(data);
	    }
            break;
	case "updated":
            App.show_info(App.code_message[data["code"]]);
            if (callback){
		callback(data);
	    }
            break;
        case "deleted":
            App.show_info(App.code_message[data["code"]]);
            callback(data);
            break;
	case "message_sent":
            App.show_info(App.code_message[data["code"]]);
	    if(callback){
		callback(data);
	    }
	    break;
	case "redirect":
	    window.location.href = data["redirect_url"];
            break;
        default:
            alert("unknown response");
        }
    },
    code_message:{"access_denied" : "You don't have access for this operation",
		  "form_error" : "The data submitted is not valid. Please make sure you have entered correct data",
		  "system_error" : "A system error has occured. Please contact the site administrator",
		  "invalid_request" : "In valid request",
		  "saved" : "Data has been saved successfully",
		  "deleted" : "Data has been deleted successfully",
		  "updated" : "Data updated",
		  "message_sent": "Message sent",
		  "access_denied":"You have to login to perform this action"
		 },

    process_error:function(errors){
        for (var i in errors){
            var error_message = "";
            for (var j in errors[i]){
                if(j>0){
                    error_message+="<br/>";
                }
                error_message += errors[i][j];
            }
            $("#message_" + i).html(error_message);
            $("#container_" + i).addClass("error");
        }
        if ("__all__" in errors){
            $("#message___all__").show();
        }
    },
    clear_form:function(ids){
        for (var i in ids){
            $("#id_"+ids[i]).attr('value','');
        }
    },
    populate_form:function(dict){
        for (var key in dict){
            $("#id_" + key).val(dict[key]);
        }
    },
    show_loader:function(loader_message, loader_id){
        if(loader_id != "None"){
            if (loader_message!="None"){
                $("#"+loader_id).html(loader_message);
            }
            $("#" + loader_id).show();
        }
    },
    hide_loader:function(loader_id){
        if(loader_id != "None"){
            $("#" + loader_id).hide();
        }
    },
    show_info:function(info_message){
        $("#info").html(info_message);
        $("#info").slideDown();
        setTimeout("App.hide_info()",3000);
    },
    hide_info:function(){
        $("#info").slideUp("slow");
        //$("#info").html("");
    },
    show_error:function(info_message){
        $("#error").html(info_message);
        $("#error").slideDown();
        setTimeout("App.hide_error()",5000);
    },
    hide_error:function(){
        $("#error").slideUp("slow");
        //$("#info").html("");
    },
    show_warning:function(info_message){
        $("#warning").html(info_message);
        $("#warning").slideDown();
        setTimeout("App.hide_warning()",3000);
    },
    hide_warning:function(){
        $("#warning").slideUp("slow");
        //$("#info").html("");
    },
    User:{
	save_user:function(){
            var obj = {"value":["user_id", "username", "password1", "password2", "email"]};
            App.submit_data(obj,{},"/app/add/user", App.User.save_user_callback, "loader");
	},
	save_user_callback:function(data){
            $("#id_user_id").val(data["user_id"]);
	},
	login:function(){
            var obj = {"value":["username", "password"],"check":["remember_me"]};
            App.submit_data(obj,{},"/app/login_user", App.User.login_callback, "loader");
	},
	login_callback:function(data){
            window.location.href = data["next_view"];
	},
	password_reset_email:function(){
	    var obj = {"value":["email"]};
            App.submit_data(obj,{},"/app/password/reset/submit/email", App.User.password_reset_email_callback, "loader");
	},
	password_reset_email_callback:function(data){
	    $("#email_form").hide();
	    $("#email_sent").show();
	},
	password_reset_password:function(data){
	    var obj = {"value":["password","confirm_password"]};
            App.submit_data(obj,{},"/app/password/reset/submit/password", App.User.password_reset_password_callback, "loader");
	},
	password_reset_password_callback:function(data){
	    location.href=data["redirect"];
	}
	
    },
    Base:{
	submit_contact:function(){
	    var obj = {"value":["name","email", "inquiry"]};
	    App.submit_data(obj, {}, "/app/contact/submit" , App.Base.submit_contact_callback, "loader");
	},
	submit_contact_callback:function(){
	    $("#contact-form").hide();
	    $("#success-message").show();
	}
    },
    Calendar:{
	start_booking:function(event){
	    $("#id_start").val(event.start);
	    event_date = event.start;
	    var day = App.Calendar.week_days[event.start.getDay()];
	    var month  = App.Calendar.month_names[event.start.getMonth()];
	    var year = event.start.getFullYear();
	    var date_day = event.start.getDate();
	    $("#start-date").html(day+" "+month+" "+date_day+" "+year);
	    $("#id_id").val("");
	    $('#modal-booking').modal({backdrop: false});
	    $('#modal-booking').modal('show');
	    //App.Calendar.calculate_amount();
	    
	},
	month_names:[ "January", "February", "March", "April", "May", "June",
		     "July", "August", "September", "October", "November", "December" ],
	week_days:["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Staurday"],
	get_start_end:function(){
	    start_date = $("#start-date").html();
	    fromTimeHour = $("#id_time_from_hour").val();
	    fromTimeMinute = $("#id_time_from_minute").val();
	    fromTimeAmPm = $("#id_time_from_ampm").val();
	    toTimeHour = $("#id_time_to_hour").val();
	    toTimeMinute = $("#id_time_to_minute").val();
	    toTimeAmPm = $("#id_time_to_ampm").val();
	    start = start_date + " " + fromTimeHour+ ":"+fromTimeMinute+fromTimeAmPm;
	    end = start_date + " " + toTimeHour+ ":"+toTimeMinute+toTimeAmPm;
	    return {"start":start, "end":end};
	},
	calculate_amount:function(){
	    start_end = App.Calendar.get_start_end();
	    App.get_data("/app/calculate/price", {start:start_end["start"], end:start_end["end"]},
			 function(data){
			     
			     $("#total-amount").html(data["price"]);
			 },
			 "calculate-amount-loader");
	    
	},
	book_event:function(){
	    start_end = App.Calendar.get_start_end();
	    $("#id_start").val(start_end["start"]);
	    $("#id_end").val(start_end["start"]);
	  
	    var obj = {"value":["start", "end", "school", "fraternity","address", "city", "state"]};
	    App.submit_data(obj,{},"/app/book/event", function(){}, "loader");
	}
    },
    Files:{
	upload_queue:[]
    },
    Util:{
	format_date_str:function(str_date){
	    if (!str_date){
		return null;
	    }
	    var date_object = $.fullCalendar.parseDate(str_date);
	    var year = date_object.getFullYear();
	    var month = date_object.getMonth() + 1;
	    var day = date_object.getDate();
	    var hour = date_object.getHours();
	    var minutes = date_object.getMinutes();
	    var date_text = year+"-"+month+"-"+day+" "+hour+":"+minutes;
	    return date_text;
	}
    }
    
};
var event_date;
