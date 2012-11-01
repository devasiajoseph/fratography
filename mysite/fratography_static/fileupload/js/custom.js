$(function () {
    $('#fileupload').fileupload({
        dataType: 'json',
        done: function (e, data) {
            $.each(data.result, function (index, file) {
                $('<p/>').text(file.name).appendTo(document.body);
            });
       
        },
	progressall: function (e, data) {
        
            var progress = parseInt(data.loaded / data.total * 100, 10);
            $('#progress .bar').css(
		'width',
		progress + '%'
            );
     
	},
	add:function(e, data){
            $.each(data.files, function (index, file) {
		console.log('Added file: ' + file.name+ "-----"+ file.size+index);
                var upload_image = new UploadImage({image: data});
		console.log(upload_image.cid);
		var image_preview1 = new ImagePreview({el:$("#image_preview_container"), file:file, upload_image:upload_image});
		upload_stack.add(upload_image);
            });
           
	}

    });
});

var UploadImage = Backbone.Model.extend({
        initialize: function(){
            
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
	 
	$("#cancel_"+this.options.upload_image.cid).bind('click', {index:this.options.upload_image.cid}, this.remove_file);
        
    },
    remove_file:function(event){
	console.log(event.data.index);
    }
});

var UploadStack = Backbone.Collection.extend({
    model: UploadImage
});
var upload_stack = new UploadStack();

function readImage(f){
    var reader = new FileReader();
    reader.onload = (function(theFile) {
        return function(e) {
            // Render thumbnail.
            var span = document.createElement('span');
            span.innerHTML = ['<img class="thumb" src="', e.target.result,
                              '" title="', escape(theFile.name), '"/>'].join('');
            document.getElementById('list').insertBefore(span, null);
        };
    })(f);
    reader.readAsDataURL(f);
}