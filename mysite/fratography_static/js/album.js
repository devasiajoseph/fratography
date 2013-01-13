
var AlbumCover = Backbone.View.extend({
    initialize:function(attrs){
	this.options = attrs;
	this.render();
	
    },
    render:function(){
	
	// Compile the template using underscore
	var album = this.options.album;
	var variables = {
	    cover_photo:album.cover_photo,
	    name:album.name,
	    album_id:album.id
	}
        var template = _.template( $("#album").html(), variables);
        // Load the compiled HTML into the Backbone "el"
        this.$el.append( template );
    }
    
});
var AlbumPhoto = Backbone.View.extend({
    initialize:function(attrs){
	this.options = attrs;
	this.render();
	
    },
    render:function(){
	
	// Compile the template using underscore
	var photo = this.options.photo;
	var variables = {
	    thumbnail:photo.thumbnail,
	    display:photo.display,
	    image_id:photo.id
	}
        var template = _.template( $("#album-photo").html(), variables);
        // Load the compiled HTML into the Backbone "el"
        this.$el.append( template );
    }
    
});

var AlbumsRow = Backbone.View.extend({
    el:$('#albums-container'),
    initialize:function(attrs){
	this.options = attrs;
	this.render();
    },
    render:function(){
	// Compile the template using underscore
	var variables = {id:this.options.id}
        var template = _.template( $("#albums-row").html(), variables);
        // Load the compiled HTML into the Backbone "el"
        this.$el.append( template );
    }
});
var AlbumRouter = Backbone.Router.extend({
    routes: {
	":album_id/:number": "process",
	"*path":  "defaultRoute"
    },
    defaultRoute:function(){
	if($("#id_college_name").val()!=""){
	    console.log("college page");
	    this.processAlbums("all", 1);
	}else if($("#id_album_subcategory")){
	    this.processAlbums("all", 1);
	}	 
	else{
	    console.log("no man's page");
	}
    },
    process:function(album_id, number){
	
	if(album_id=="all"){
	    this.processAlbums(album_id, number);
	}else{
	    this.processPhotos(album_id, number);
	}
    },
    processAlbums:function(album_id, number){
	$("#albums-container").html("");
	college_name = $("#id_college_name").val();
	subcategory_name = $("#id_subcategory_name").val();
	count = count = $("#show-count").val();
	var data = {page: number,
		    show: count,
		    album_id:album_id,
		    college_name:college_name,
		    subcategory_name:subcategory_name};
	
	create_album_row(count);
	App.get_raw_data("/app/album/objects", data, function(data){
	    for (i in data["data"]){
		create_album_cover(data["data"][i], parseInt(i/3, 10));
	    }
	    create_paginator(album_id,
			     number,
			     count,
			     data["total_count"],
			    ":album_id/:number");
	}, "album-loader");
	
	
    },
    processPhotos:function(album_id, number){
	$("#albums-container").html("");
	count = $("#show-count").val();
	college_name = $("#id_college_name").val();
	var send_data = {page: number, show: count, album_id:album_id, college_name:college_name};
	
	create_album_row(count);
	App.get_raw_data("/app/album/photos", send_data, function(data){
	    for (i in data["data"]){
		create_album_photo(data["data"][i], parseInt(i/4, 10));
	    }
	    create_paginator(album_id,
			     number,
			     count,
			     data["total_count"],
			    ":album_id/:number");
	}, "album-loader");
	
    }
});
function create_album_row(count){
    
    var totalRows = parseInt(count/3, 10);
    if (count/3>totalRows){
	totalRows = totalRows + 1;
    }
    
    for(i=0;i<totalRows;i++){
	var album_row = new AlbumsRow({"id":i});
    }
}

function create_album_cover(album, row_id){
    
    var album_cover = new AlbumCover({
	el: $("#albums-row-"+row_id),
	"album":album});
}
function create_album_photo(photo, row_id){
    var album_photo = new AlbumPhoto({
	el: $("#albums-row-"+row_id),
	"photo":photo});
}
function create_paginator(album_id, number, count, total_count, url_pattern){
    $("#pagination-container").html("");
    total_pages = parseInt(total_count/count, 10);
    if (total_count/count>total_pages){
	total_pages = total_pages + 1;
    }
    
    for(i=1;i<=total_pages;i++){
	var pageNumber = new PageNumber(
	    {
		"album_id":album_id,
		"number":number,
		"count":i,
		"url_pattern":url_pattern}
	);
    }
}
var PageNumber = Backbone.View.extend({
    
    tagName: "a",
    el:$('#pagination-container'),
    initialize:function(attrs){
	this.options = attrs;
	this.render();
	
    },

    events: {
	"click":"page",
    },
    

    render:function(){
	url_link = this.options.url_pattern.replace(":number", this.options.count);
	url_link = url_link.replace(":album_id", this.options.album_id);
	
	if (this.options.count == this.options.number){
	    this.$el.append('<li class="active"><a class="act" href="#'+url_link+'">'+this.options.count+'</a></li>')
	}else{
	    this.$el.append('<li><a href="#'+url_link+'">'+this.options.count+'</a></li>')
	    }
    },
    page:function(){
	//console.log(this.options.number);
    }

});

function displayImage(image){
    $("#display-image").hide();
    $("#display-image").attr('src', image);
    $("#image-modal").modal({keyboard: true});
    $("#image-modal").css('width','600px');
    //$("#display-image-container").html('<img src="'+image+'" id="display-image" onload="adjustImageModal()">');
    
}

function adjustImageModal(){
    
   // $("#image-modal").css('height',$("#display-image").height()+'px');
   // $("#image-modal").css('width',$("#display-image").width()+'px');
}
var album_router = new AlbumRouter;
Backbone.history.start();

$("#image-modal").on('shown',
		     function(){
			 $("#image-modal").css('width',$("#display-image").width()+'px');
			 $("#display-image").show();
			 console.log($("#display-image").width());
		     });
function vote(vote, object_id, vote_type){
    var loader = "loader";
    if (vote_type=="album"){
	loader = "album_cover_loader_"+object_id;
    }else{
	loader = "album_image_loader_"+object_id;
    }
    submit_obj = {"vote":vote, "object_id":object_id, "vote_type":vote_type};
    App.submit_data({}, submit_obj, "/app/vote", function(data){alert(data["code"]);},loader);
}
