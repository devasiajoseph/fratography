$(function () {
    $('#fileupload').fileupload({
        dataType: 'json',
        done: function (e, data) {
	    console.log(data);
            $.each(data.result, function (index, file) {
		var upload_image = new UploadImage({image: file});
		var uploaded_image_preview = new UploadedImagePreview({el:$("#image_preview_container"), upload_image:upload_image});
		$("#upload_container_"+file.cid).remove();
		image_data = upload_stack.getByCid(file.cid);
		upload_stack.remove(image_data);
            });
	    
       
        },
	progressall: function (e, data) {
        
            var progress = parseInt(data.loaded / data.total * 100, 10);
            $('#progress .bar').css(
		'width',
		progress + '%'
            );
     
	},
	prograss:function(e, data){
	    console.log(data.loaded);
	},
	add:function(e, data){
            $.each(data.files, function (index, file) {
		console.log('Added file: ' + file.name+ "-----"+ file.size+index);
                var upload_image = new UploadImage({image: data});
		console.log(upload_image.cid);
		var image_preview = new ImagePreview({el:$("#image_preview_container"), file:file, upload_image:upload_image});
		upload_stack.add(upload_image);
            });
           
	}

    });
});

var UploadImage = Backbone.Model.extend({
    urlRoot:'/admin/album/image',
    initialize: function(){
        
    },
    delete:function(){
	
    }
});

var UploadedImagePreview = Backbone.View.extend({
    initialize: function(attrs){
	this.options = attrs;
	this.render();
    },
    render:function(){
	var variables = { preview:this.options.upload_image.get("image").preview, id: this.options.upload_image.get("image").id};
        // Compile the template using underscore
        var template = _.template( $("#image_uploaded_template").html(), variables );
        // Load the compiled HTML into the Backbone "el"
        this.$el.append( template );
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
	this.each(function(data){
	    console.log(data.cid)
	    $("#cid").val(data.cid);
	    data.get('image').submit();
	});
    }
});
var upload_stack = new UploadStack();
var total_size = 0;
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