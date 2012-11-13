$(function () {
    if($("#id_album_id").val()){
	
	$("#images_container_widget").show();
	$("#album_delete_button").show();
	//load uploaded images
	get_album_images();
    }
    $('#fileupload').fileupload({
        dataType: 'json',
        done: function (e, data) {
	    //console.log(data);
	    uploaded_files = uploaded_files + 1;
	    if (total_files_to_upload==uploaded_files){
		console.log("upload_complete");
		total_files_to_upload = 0;
		uploaded_files = 0;
		set_progress(100);
	    }
            $.each(data.result, function (index, file) {
		var upload_image = upload_stack.getByCid(file.cid);
		upload_image.set({image:data});
		upload_image.set({file:file})
		upload_image.set({isUploaded:true});
		var uploaded_image_preview = new UploadedImagePreview({el:$("#image_preview_container"), upload_image:upload_image, id:file.id});
		$("#upload_container_"+file.cid).remove();
		
            });
	    
       
        },
	progressall: function (e, data) {
        
            var progress = parseInt(data.loaded / data.total * 100, 10);
            set_progress(progress);
     
	},
	progress:function(e, data){
	    //console.log("each-----"+data.loaded);
	    var progress = parseInt(data.loaded / data.total * 100, 10);
	    
	},
	add:function(e, data){
            $.each(data.files, function (index, file) {
		//console.log('Added file: ' + file.name+ "-----"+ file.size+index);
                var upload_image = new UploadImage({image: data});
		//console.log(upload_image.cid);
		var image_preview = new ImagePreview({el:$("#image_preview_container"), file:file, upload_image:upload_image});
		upload_stack.add(upload_image);
            });
           
	}

    });
});

var UploadImage = Backbone.Model.extend({
    urlRoot:'/admin/album/image',
    initialize: function(){
        this.set({isUploaded:false});
    },
    delete_file:function(event){
	//console.log(event.data.id);
	var submit_obj = {"image_id":event.data.id, "image_cid":event.data.cid};
        App.submit_data({},submit_obj,"/admin/album/image/delete",
			function(data){
			    //console.log(data.cid);
			    upload_image = upload_stack.getByCid(data.cid);
			    upload_stack.remove(upload_image);
			    $("#upload_container_"+data.id).remove()
			},
			"image_loader_"+event.data.id);
	
    },
    isUploaded:false
});

var UploadedImagePreview = Backbone.View.extend({
    initialize: function(attrs){
	this.options = attrs;
	this.render();
    },
    render:function(){
	var variables = { preview:this.options.upload_image.get("file").preview, id: this.options.id};
        // Compile the template using underscore
        var template = _.template( $("#image_uploaded_template").html(), variables );
        // Load the compiled HTML into the Backbone "el"
        this.$el.append( template );
	//console.log(this.options.id);
	$("#delete_"+this.options.id).bind('click',
					   {id:this.options.id,
					    cid:this.options.upload_image.cid },
					   this.options.upload_image.delete_file);
    },
    delete_file:function(event){
	//console.log(event.data.upload_image.cid);
	upload_stack.getByCid(event.data.upload_image.cid).delete_file();
    }
    
});
var ImagePreview = Backbone.View.extend({
    initialize: function(attrs){
	this.options = attrs;
	this.render();
    },
    render:function(){
	//console.log(this.options.data);
	var variables = { file: this.options.file, index:this.options.upload_image.cid };
        // Compile the template using underscore
        var template = _.template( $("#image_preview_template").html(), variables );
        // Load the compiled HTML into the Backbone "el"
        this.$el.append( template );
	 
	$("#cancel_"+this.options.upload_image.cid).bind('click', {upload_image:this.options.upload_image}, this.remove_file);
	$("#upload_"+this.options.upload_image.cid).bind('click', {upload_image:this.options.upload_image}, this.upload_file);
	readImage(this.options.upload_image.get('image').files[0], "image_"+this.options.upload_image.cid)
        
    },
    remove_file:function(event){
	upload_stack.remove(event.data.upload_image);
	$("#upload_container_"+event.data.upload_image.cid).remove()
    },
    upload_file:function(event){	
	event.data.upload_image.get('image').submit();
    }
});

var UploadStack = Backbone.Collection.extend({
    model: UploadImage,
    total_size:function(){
	total_size = 0;
	this.each(function(data){
	    total_size = total_size + data.get('image').files[0].size;
	});
    },
    upload_all:function(){
	reset_progress();
	this.each(function(data){
	    if(!data.get('isUploaded')){
		total_files_to_upload = total_files_to_upload + 1;
		
	    }
	});
	this.each(function(data){
	    //console.log(data.cid);
	    //console.log(data.get('image'));
	    if(!data.get('isUploaded')){
		$("#cid").val(data.cid);
		data.get('image').submit();
	    }
	});
    }
});
var upload_stack = new UploadStack();
var total_files_to_upload = 0;
var uploaded_files = 0;
function readImage(f, id){
    var reader = new FileReader();
    reader.onload = (function(theFile) {
        return function(e) {
            // Render thumbnail.
	    $("#"+id).attr('src', e.target.result);
        };
    })(f);
    reader.readAsDataURL(f);
}

function get_album_images(){
    var album_id = $("#id_album_id").val();
    App.get_raw_data("/admin/get/album/images/"+album_id, {},function(data){
	for (i in data){
	    setupUploadedImage(data[i]);
	}
    }, "loader")
}

function setupUploadedImage(data){
    file = data.fields;
    var upload_image = new UploadImage();
    //console.log(upload_image.cid);
    upload_image.set({id:data.pk});
    upload_image.set({file:file});
    upload_image.set({isUploaded:true});
    upload_stack.add(upload_image);
    var uploaded_image_preview = new UploadedImagePreview({el:$("#image_preview_container"), upload_image:upload_image, id:data.pk});
}

function set_progress(progress){
    $('#progress .bar').css('width', progress + '%');
    if (progress==100){
	$('#progress').removeClass('progress-striped');
    };
    $("#show-progress").html(progress+"%");
}
function reset_progress(){
    $('#progress .bar').css('width','0%');
    $('#progress').addClass('progress-striped');
}
